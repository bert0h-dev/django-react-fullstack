from rest_framework import viewsets, permissions, status
from rest_framework.views  import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.contrib.auth import authenticate, get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from core.utils.models import get_model_name
from core.responses import api_success, api_error
from core.decorators import log_view_action
from core.permissions import IsAdminOrStaff
from core.messages import ACCOUNT_LOG, ACCOUNT_SUCCESS, ACCOUNT_ERRORS

from .models import User
from .filters import UserFilter
from .serializers import LoginSerializer, LogoutSerializer, UserSerializer, RefreshTokenSerializer, ChangePasswordSerializer

User = get_user_model()

@extend_schema(
  summary="Cambiar contraseña del usuario autenticado",
  description="Permite cambiar la contraseña del usuario autenticado. Se requiere proporcionar la contraseña actual y la nueva contraseña.",
  request=ChangePasswordSerializer,
  responses={200: None},
)
class ChangePasswordView(APIView):
  def post(self, request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return api_success(message="Contraseña cambiada correctamente")

@extend_schema(
  summary="Gestión de usuarios",
  description="Listar, actualizar o eliminar usuarios del sistema.",
  parameters=[
    OpenApiParameter(name='email', description='Filtrar por email', required=False, type=str),
    OpenApiParameter(name='first_name', description='Filtrar por nombre', required=False, type=str),
    OpenApiParameter(name='last_name', description='Filtrar por apellido', required=False, type=str),
    OpenApiParameter(name='is_active', description='Filtrar por estado activo', required=False, type=bool),
  ]
)
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAdminOrStaff]
  filter_backends = [DjangoFilterBackend]
  filterset_class = UserFilter

  @log_view_action(ACCOUNT_LOG["user_list"])
  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      paginated_data = self.get_paginated_response(serializer.data).data
      return api_success(data=paginated_data, message=ACCOUNT_SUCCESS["user_list"])

    serializer = self.get_serializer(queryset, many=True)
    return api_success(data=serializer.data, message=ACCOUNT_SUCCESS["user_list"])
  
  @log_view_action(ACCOUNT_LOG["user_details"])
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return api_success(data=serializer.data, message=ACCOUNT_SUCCESS["user_details"])
  
  @log_view_action(
    ACCOUNT_LOG["user_create"], 
    object_getter=lambda self, request, kwargs: self.get_object().email,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return api_success(data=serializer.data, message=ACCOUNT_SUCCESS["user_create"], status_code=status.HTTP_201_CREATED)

  @log_view_action(
    ACCOUNT_LOG["user_update"],
    object_getter=lambda self, request, kwargs: self.get_object().email,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return api_success(data=serializer.data, message=ACCOUNT_SUCCESS["user_update"])
  
  @log_view_action(ACCOUNT_LOG["user_destroy"])
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return api_success(message=ACCOUNT_SUCCESS["user_destroy"], status_code=status.HTTP_204_NO_CONTENT)

@extend_schema(
  summary="Iniciar sesión",
  description="Permite a un usuario autenticarse y obtener tokens JWT.",
  request=LoginSerializer,
  responses={200: LoginSerializer},
)
class LoginView(TokenObtainPairView):
  auuthentication_classes = []
  permission_classes = [permissions.AllowAny]

  @log_view_action(ACCOUNT_LOG["login"])
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(request, username=email, password=password)

    if user is None:
      return api_error(message=ACCOUNT_ERRORS["invalid_credentials"], status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
      return api_error(message=ACCOUNT_ERRORS["account_disabled"], status_code=status.HTTP_403_FORBIDDEN)
      
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    data = {
      "access": access_token,
      "refresh": refresh_token,
      "user": {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": user.user_type,
      }
    }

    return api_success(data=data, message=ACCOUNT_SUCCESS["login"])

@extend_schema(
    summary="Cerrar sesión",
    description="Permite invalidar el token de refresh del usuario.",
    request=LogoutSerializer,
    responses={205: None}
)
class LogoutView(APIView):
  @log_view_action(ACCOUNT_LOG["logout"])
  def post(self, request):
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
      refresh_token = request.data.get("refresh")
      token = RefreshToken(refresh_token)
      token.blacklist()
      return api_success(message=ACCOUNT_SUCCESS["logout"], status_code=status.HTTP_205_RESET_CONTENT)
    except TokenError:
      return api_error(message=ACCOUNT_ERRORS["token_invalid"], status_code=status.HTTP_400_BAD_REQUEST)

@extend_schema(
  summary="Refrescar token de acceso",
  description="Permite obtener un nuevo access token usando un refresh token válido.",
  request=RefreshTokenSerializer,
  responses={200: RefreshTokenSerializer}
)
class RefreshTokenView(APIView):
  permission_classes = [permissions.AllowAny]
  authentication_classes = []  # No se necesita estar logueado para refrescar
  
  @log_view_action(ACCOUNT_LOG["token_refresh"])
  def post(self, request):
    serializer = RefreshTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    refresh_token = serializer.validated_data.get("refresh")

    try:
      refresh = RefreshToken(refresh_token)
      access_token = str(refresh.access_token)
      data = {
        "access": access_token,
      }
      return api_success(data=data, message=ACCOUNT_SUCCESS["token_refresh"])
    except TokenError:
      return api_error(message=ACCOUNT_ERRORS["token_invalid"], status_code=status.HTTP_401_UNAUTHORIZED)
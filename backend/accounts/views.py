from rest_framework import generics, permissions, status
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema, OpenApiParameter

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from core.responses import api_success, api_error
from .models import User
from .filters import UserFilter
from .serializers import (
  UserSerializer, 
  RegisterSerializer, 
  CustomTokenObtainPairSerializer,
  LogoutSerializer
)

User = get_user_model()

@extend_schema(
  summary="Listar usuarios del sistema",
  description="Permite obtener una lista paginada de usuarios con filtros por email, nombre(s), apellido(s), estado activo y estado verificado.",
  parameters=[
    OpenApiParameter(name='email', description='Filtrar por email', required=False, type=str),
    OpenApiParameter(name='first_name', description='Filtrar por primer nombre', required=False, type=str),
    OpenApiParameter(name='last_name', description='Filtrar por segundo nombre', required=False, type=str),
    OpenApiParameter(name='first_surname', description='Filtrar por primer apellido', required=False, type=str),
    OpenApiParameter(name='last_surname', description='Filtrar por segundo apellido', required=False, type=str),
    OpenApiParameter(name='is_active', description='Filtrar por estado activo', required=False, type=bool),
    OpenApiParameter(name='is_verified', description='Filtrar por estado verificado', required=False, type=bool),
  ],
  request=UserSerializer,
  responses={200: UserSerializer(many=True)}
)
class UserListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.AllowAny]
  filter_backends = [DjangoFilterBackend]
  filterset_class = UserFilter

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      paginated_data = self.get_paginated_response(serializer.data).data
      return api_success(data=paginated_data, message="Lista de usuarios", status_code=status.HTTP_200_OK)
    
    # Si no hay paginación, se devuelve la lista completa
    serializer = self.get_serializer(queryset, many=True)
    return api_success(data=serializer.data, message="Lista de usuarios", status_code=status.HTTP_200_OK)

@extend_schema(
  summary="Registrar un nuevo usuario",
  description="Permite registrar un nuevo usuario en el sistema. Se requiere proporcionar email, nombre(s), apellido(s) y contraseña.",
  request=RegisterSerializer,
  responses={201: RegisterSerializer},
)
class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny]

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    # Se devuelve el usuario + el token
    data = serializer.data
    data['tokens'] = serializer._tokens

    return api_success(data=data, message="Usuario registrado correctamente", status_code=status.HTTP_201_CREATED)

@extend_schema(
  summary="Obtener token de acceso",
  description="Permite obtener un token de acceso y un token de actualización para el usuario autenticado. Se requiere proporcionar email y contraseña.",
  request=CustomTokenObtainPairSerializer,
  responses={200: RegisterSerializer},
)
class LoginView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer

  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    response.data["message"] = "Inicio de sesión exitoso"
    return Response(response.data, status_code=status.HTTP_200_OK)

@extend_schema(
  summary="Cerrar sesión",
  description="Permite cerrar la sesión del usuario autenticado. Se requiere proporcionar el token de actualización.",
  request=LogoutSerializer,
  responses={205: LogoutSerializer},
)
class LogoutView(APIView):
  serializer_class = LogoutSerializer

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
      refresh_token = serializer.validated_data["refresh"]
      token = RefreshToken(refresh_token)
      token.blacklist()
      return api_success(message="Sesión cerrada correctamente", status_code=status.HTTP_205_RESET_CONTENT)
    except TokenError:
      return api_error(message="Token inválido o ya ha sido cerrado", status_code=status.HTTP_400_BAD_REQUEST)
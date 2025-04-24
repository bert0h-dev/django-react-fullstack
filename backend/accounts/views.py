from rest_framework import generics, permissions, status
from rest_framework.views  import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from core.utils.models import get_model_name
from core.models import AccessTokenBlacklist
from core.responses import api_success, api_error
from core.decorators import log_view_action
from core.permissions import CanViewGroup

from .models import User
from .filters import UserFilter
from .serializers import (
  # Autenticación
  LoginSerializer, LogoutSerializer,
  # Usuarios
  UserSerializer, RegisterSerializer, 
  UserProfileSerializer, UpdateProfileSerializer,
  ChangePasswordSerializer,
  # Roles
  AssignRolesSerializer, UserRolesSerializer
)

User = get_user_model()

@extend_schema(
  summary="Listar usuarios del sistema",
  description="Permite obtener una lista paginada de usuarios con filtros por email, nombre(s), apellido(s), estado activo, verificado y tipo de usuario.",
  parameters=[
    OpenApiParameter(name='email', description='Filtrar por email', required=False, type=str),
    OpenApiParameter(name='first_name', description='Filtrar por primer nombre', required=False, type=str),
    OpenApiParameter(name='last_name', description='Filtrar por segundo nombre', required=False, type=str),
    OpenApiParameter(name='first_surname', description='Filtrar por primer apellido', required=False, type=str),
    OpenApiParameter(name='last_surname', description='Filtrar por segundo apellido', required=False, type=str),
    OpenApiParameter(name='is_active', description='Filtrar por estado activo', required=False, type=bool),
    OpenApiParameter(name='is_verified', description='Filtrar por estado verificado', required=False, type=bool),
    OpenApiParameter(name='user_type', description='Filtrar por tipo de usuario', required=False, type=str),
  ],
  request=UserSerializer,
  responses={200: UserSerializer(many=True)}
)
class UserListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  filter_backends = [DjangoFilterBackend]
  filterset_class = UserFilter

  @log_view_action("Visualizó el listado de usuarios")
  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      paginated_data = self.get_paginated_response(serializer.data).data
      return api_success(data=paginated_data, message="Lista de usuarios")
    
    # Si no hay paginación, se devuelve la lista completa
    serializer = self.get_serializer(queryset, many=True)

    return api_success(data=serializer.data, message="Lista de usuarios")

@extend_schema(
  summary="Obtener el perfil del usuario autenticado",
  description="Permite obtener el perfil del usuario autenticado. Se requiere autenticación.",
  responses={200: UserProfileSerializer},
)
class MeView(APIView):

  @log_view_action(
    "Visualizó perfil de usuario",
    object_getter=lambda self, request, kwargs: self.get_object().email,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def get(self, request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return api_success(data=serializer.data, message="Perfil de usuario")

@extend_schema(
  summary="Actualizar perfil del usuario",
  description="Permite al usuario autenticado modificar sus datos de perfil como nombres, apellidos y zona horaria.",
  request=UpdateProfileSerializer,
  responses={200: UserProfileSerializer}
)
class UpdateProfileView(generics.UpdateAPIView):
  serializer_class = UpdateProfileSerializer
  
  def get_object(self):
    return self.request.user
  
  def patch(self, request, *args, **kwargs):
    response = super().partial_update(request, *args, **kwargs)
    user = self.get_object()
    return api_success(data=UserProfileSerializer(user).data, message="Perfil actualizado correctamente")

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
    serializer.save()
    # Se devuelve el usuario + el token
    data = serializer.data
    data['tokens'] = serializer._tokens
    return api_success(data=data, message="Usuario registrado correctamente", status_code=status.HTTP_201_CREATED)

@extend_schema(
  summary="Asignar roles a un usuario",
  description="Permite asignar uno o más grupos (roles) a un usuario.",
  request=AssignRolesSerializer,
  responses={200: AssignRolesSerializer}
)
class AssignRolesToUserView(generics.UpdateAPIView):
  queryset = User.objects.all()
  serializer_class = AssignRolesSerializer
  permission_classes = [CanViewGroup]
  lookup_url_kwarg = "id"

  def patch(self, request, *args, **kwargs):
    response = super().partial_update(request, *args, **kwargs)
    return api_success(data=response.data, message="Roles asignados correctamente")

@extend_schema(
  summary="Consultar roles asignados a un usuario",
  description="Devuelve los grupos (roles) actualmente asignados a un usuario.",
  responses={200: UserRolesSerializer}
)
class UserRolesView(generics.RetrieveAPIView):
  queryset = User.objects.prefetch_related("groups")
  serializer_class = UserRolesSerializer
  permission_classes = [CanViewGroup]
  lookup_url_kwarg = "id"

  def retrieve(self, request, *args, **kwargs):
    user = self.get_object()
    serializer = self.get_serializer(user)
    return api_success(data=serializer.data, message="Roles del usuario")

@extend_schema(
  summary="Obtener token de acceso",
  description="Permite obtener un token de acceso y un token de actualización para el usuario autenticado. Se requiere proporcionar username y contraseña.",
  request=LoginSerializer,
  responses={200: RegisterSerializer},
)
class LoginView(TokenObtainPairView):
  serializer_class = LoginSerializer
  permission_classes = [permissions.AllowAny]

  @log_view_action("Inicio de sesión")
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    return api_success(data=response.data, message="Inicio de sesión exitoso")

@extend_schema(
  summary="Cerrar sesión",
  description="Cierra sesión invalidando el refresh token y el access token actual.",
  request=LogoutSerializer,
  responses={205: LogoutSerializer},
)
class LogoutView(APIView):
  serializer_class = LogoutSerializer

  @log_view_action("Cierre de sesión")
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
      # 🔒 1. Invalidar el refresh token
      refresh_token = serializer.validated_data["refresh"]
      token = RefreshToken(refresh_token)
      token.blacklist()

      # 🔒 2. Invalidar el access token actual usando su jti
      access_token = request.auth 
      jti = access_token.get("jti")
      AccessTokenBlacklist.objects.get_or_create(token=jti)

      return api_success(message="Sesión cerrada correctamente", status_code=status.HTTP_205_RESET_CONTENT)
    except TokenError:
      return api_error(message="Token inválido o ya ha sido cerrado", status_code=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate

from core.decorators import log_view_action
from core.responses import api_success, api_error
from core.messages import MSG_LOGS, MSG_SUCCESS, MSG_ERRORS

from accounts.serializers.s_authentication import LoginSerializer, LogoutSerializer, RefreshTokenSerializer

@extend_schema(
  summary="Iniciar sesión",
  description="Permite a un usuario autenticarse y obtener tokens JWT.",
  request=LoginSerializer,
  responses={200: LoginSerializer},
)
class LoginView(TokenObtainPairView):
  auuthentication_classes = []
  permission_classes = [AllowAny]

  @log_view_action(MSG_LOGS["login"])
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(request, username=email, password=password)

    if user is None:
      return api_error(message=MSG_ERRORS["invalid_credentials"], status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
      return api_error(message=MSG_ERRORS["account_disabled"], status_code=status.HTTP_403_FORBIDDEN)
      
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

    return api_success(data=data, message=MSG_SUCCESS["login"])

@extend_schema(
    summary="Cerrar sesión",
    description="Permite invalidar el token de refresh del usuario.",
    request=LogoutSerializer,
    responses={205: None}
)
class LogoutView(APIView):
  @log_view_action(MSG_LOGS["logout"])
  def post(self, request):
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
      refresh_token = request.data.get("refresh")
      token = RefreshToken(refresh_token)
      token.blacklist()
      return api_success(message=MSG_SUCCESS["logout"], status_code=status.HTTP_205_RESET_CONTENT)
    except TokenError:
      return api_error(message=MSG_ERRORS["token_invalid"], status_code=status.HTTP_400_BAD_REQUEST)

@extend_schema(
  summary="Refrescar token de acceso",
  description="Permite obtener un nuevo access token usando un refresh token válido.",
  request=RefreshTokenSerializer,
  responses={200: RefreshTokenSerializer}
)
class RefreshTokenView(APIView):
  permission_classes = [AllowAny]
  authentication_classes = []  # No se necesita estar logueado para refrescar
  
  @log_view_action(MSG_LOGS["token_refresh"])
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
      return api_success(data=data, message=MSG_SUCCESS["token_refresh"])
    except TokenError:
      return api_error(message=MSG_ERRORS["token_invalid"], status_code=status.HTTP_401_UNAUTHORIZED)
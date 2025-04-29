from rest_framework import status
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model

from core.messages import MSG_LOGS, MSG_SUCCESS, MSG_ERRORS
from core.responses import api_success, api_error
from core.decorators import log_view_action
from core.permissions import IsAdminOrStaff
from core.utils.models import get_model_name

from accounts.serializers.s_permissions import PermissionAssignUserSerializer

User = get_user_model()

@extend_schema(
    summary="Asignar permisos a usuario",
    description="Permite asignar una lista de permisos directamente a un usuario sin necesidad de roles."
)
class PermissionAssignUserView(GenericAPIView):
  serializer_class = PermissionAssignUserSerializer
  permission_classes = [IsAdminOrStaff]

  @log_view_action(
    MSG_LOGS["permission_assign"],
    object_getter=lambda self, request, kwargs: self.get_object().name,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def post(self, request, user_id, *args, **kwargs):
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return api_error(message=MSG_ERRORS["user_do_not_exists"], status_code=status.HTTP_400_BAD_REQUEST)
    
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user)
    return api_success(data=serializer.data, message=MSG_SUCCESS["permission_assign"])
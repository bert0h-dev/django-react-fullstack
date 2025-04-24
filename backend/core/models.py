from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class AccessTokenBlacklist(models.Model):
  """
  Modelo para almacenar los tokens de acceso revocados
  """

  token = models.CharField(max_length=255, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at']
    db_table = 'core_token_blacklist'
    indexes = [
      models.Index(fields=['token'], name='idx_core_token'),
      models.Index(fields=['created_at'], name='idx_core_token_created_at'),
    ]
  def __str__(self):
    return f"AccessTokenBlacklist(token={self.token}, created_at={self.created_at})"
  
class AccessLog(models.Model):
  """
  Modelo para almacenar los logs de acceso
  """

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='access_logs')
  ip_address = models.GenericIPAddressField()
  action = models.CharField(max_length=255)
  timestamp = models.DateTimeField(auto_now_add=True)
  user_agent = models.CharField(max_length=255, blank=True, null=True)
  object_id = models.PositiveIntegerField(null=True, blank=True)
  object_type = models.CharField(max_length=50, null=True, blank=True)

  class Meta:
    verbose_name = "log de acceso"
    verbose_name_plural = "logs de acceso"
    ordering = ['-timestamp']
    db_table = 'core_access_log'
    indexes = [
      models.Index(fields=['timestamp'], name='idx_core_timestamp'),
    ]
  def __str__(self):
    return f"AcessLog(user={self.user}, action={self.action}, timestamp={self.timestamp})"
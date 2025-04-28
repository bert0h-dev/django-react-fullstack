from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Modelo para almacenar los logs de acceso
class AccessLog(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='access_logs')
  method = models.CharField(max_length=10)
  path = models.CharField(max_length=500)
  action = models.CharField(max_length=500)
  status_code = models.PositiveIntegerField(null=True, blank=True)
  message = models.CharField(max_length=500, null=True, blank=True)
  ip_address = models.GenericIPAddressField(null=True, blank=True)
  user_agent = models.CharField(max_length=255, blank=True, null=True)
  object_id = models.PositiveIntegerField(null=True, blank=True)
  object_type = models.CharField(max_length=50, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = "Registro de acceso"
    verbose_name_plural = "Registros de acceso"
    ordering = ['-created_at']
    db_table = 'core_access_log'
    
  def __str__(self):
    return f"{self.user} - {self.method} {self.path} ({self.status_code})"
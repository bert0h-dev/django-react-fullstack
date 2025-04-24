from django.db import models

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
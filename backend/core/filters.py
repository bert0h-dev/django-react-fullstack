import django_filters
from core.models import AccessLog

class AccessLogFilter(django_filters.FilterSet):
  created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', label='Desde fecha y hora')
  created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', label='Hasta fecha y hora')
  action = django_filters.CharFilter(field_name='action', lookup_expr='icontains', label='Acción contiene')
  path = django_filters.CharFilter(field_name='path', lookup_expr='icontains', label='Ruta contiene')
  user = django_filters.NumberFilter(field_name='user_id', label='ID del usuario')
  method = django_filters.CharFilter(field_name='method', lookup_expr='exact', label='Método HTTP')
  status_code = django_filters.NumberFilter(field_name='status_code', label='Código de respuesta')

  class Meta:
      model = AccessLog
      fields = ['user', 'method', 'status_code', 'action', 'path', 'created_at__gte', 'created_at__lte']
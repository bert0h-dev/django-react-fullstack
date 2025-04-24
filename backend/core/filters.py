from django_filters import rest_framework as filters
from .models import AccessLog

class AccessLogFilter(filters.FilterSet):
  user = filters.NumberFilter(field_name="user__id")
  ip_address = filters.CharFilter(lookup_expr='icontains')
  action = filters.CharFilter(lookup_expr='icontains')
  object_type = filters.CharFilter(lookup_expr='icontains')
  date = filters.DateFromToRangeFilter(field_name="timestamp")

  class Meta:
    model = AccessLog
    fields = ['user', 'ip_address', 'action', 'object_type', 'date']
import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFilter(django_filters.FilterSet):
  email = django_filters.CharFilter(lookup_expr='icontains')
  first_name = django_filters.CharFilter(lookup_expr='icontains')
  last_name = django_filters.CharFilter(lookup_expr='icontains')
  first_surname = django_filters.CharFilter(lookup_expr='icontains')
  last_surname = django_filters.CharFilter(lookup_expr='icontains')
  is_active = django_filters.BooleanFilter()
  is_verified = django_filters.BooleanFilter()

  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'first_surname', 'last_surname', 'is_active', 'is_verified']
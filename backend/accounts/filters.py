import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFilter(django_filters.FilterSet):
  email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
  first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")
  last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains")
  is_active = django_filters.BooleanFilter(field_name="is_active")

  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'is_active']
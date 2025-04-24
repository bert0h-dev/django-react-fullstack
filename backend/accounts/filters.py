import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFilter(django_filters.FilterSet):
  class Meta:
    model = User
    fields = {
      'email': ['icontains'], 
      'first_name': ['icontains'], 
      'last_name': ['icontains'], 
      'first_surname': ['icontains'], 
      'last_surname': ['icontains'], 
      'is_active': ['exact'], 
      'is_verified': ['exact'],
      'user_type': ['exact'],
    }
from django.urls import path

from .views import (
  # Logs
  AccessLogListView, 
  # Roles
  RolesDetailView,
  RolesListView, RolesCreateView, 
  RolesUpdateView, RolesDeleteView
)

urlpatterns = [
  # Roles
  path("roles/list/", RolesListView.as_view(), name="roles-list"),
  path("roles/<int:id>/detail/", RolesDetailView.as_view(), name="role-detail"),
  path("roles/create/", RolesCreateView.as_view(), name="roles-create"),
  path("roles/update/<int:pk>/", RolesUpdateView.as_view(), name="roles-update"),
  path("roles/delete/<int:pk>/", RolesDeleteView.as_view(), name="roles-delete"),
  # Logs
  path("logs/list/", AccessLogListView.as_view(), name="log-list"),
]
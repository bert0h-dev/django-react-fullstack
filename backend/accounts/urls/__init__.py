from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls.u_authentication')),
    path('users/', include('accounts.urls.u_users')),
    path('users/', include('accounts.urls.u_assign_user')),
    path('roles/', include('accounts.urls.u_roles')),
]
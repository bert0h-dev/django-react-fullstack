from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.factories import UserFactory

User = get_user_model()

class UserViewSetTests(APITestCase):
  def setUp(self):
    # Crear usuario admin
    self.admin_user = User.objects.create_superuser(
      email='admin@example.com',
      username='admin',
      password='AdminPassword123',
      first_name='Admin',
      last_name='User',
    )

    # Crear usuario normal
    self.normal_user = User.objects.create_user(
      email='user@example.com',
      username='user',
      password='UserPassword123',
      first_name='Normal',
      last_name='User',
    )

    self.login_url = reverse('login')
    self.user_list_url = '/api/accounts/users/'

    # Login como admin
    login_response = self.client.post(self.login_url, {
      'email': 'admin@example.com',
      'password': 'AdminPassword123'
    }, format='json')

    self.access_token = login_response.data['data']['access']
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

  def test_list_users(self):
    response = self.client.get(self.user_list_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('results', response.data['data'])  # Validamos paginación
    self.assertGreaterEqual(len(response.data['data']['results']), 1)

  def test_filter_users_by_email(self):
    response = self.client.get(self.user_list_url, {'email': 'admin'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(any('admin@example.com' in u['email'] for u in response.data['data']['results']))

  def test_create_user_successful(self):
    create_data = {
      "email": "newuser@example.com",
      "username": "newuser",
      "password": "NewUserPass123",
      "first_name": "Nuevo",
      "last_name": "Usuario",
      "user_type": "user"
    }
    response = self.client.post(self.user_list_url, create_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['data']['email'], "newuser@example.com")
    self.assertEqual(response.data['data']['first_name'], "Nuevo")
    self.assertEqual(response.data['data']['last_name'], "Usuario")

  def test_create_user_missing_required_fields(self):
    incomplete_data = {
      "email": "baduser@example.com"
      # Falta password, first_name, username
    }
    response = self.client.post(self.user_list_url, incomplete_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('password', response.data['data'])
    self.assertIn('first_name', response.data['data'])
    self.assertIn('username', response.data['data'])

  def test_update_user(self):
    url = f"{self.user_list_url}{self.normal_user.id}/"
    update_data = {
      'first_name': 'UpdatedName'
    }
    response = self.client.patch(url, update_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['data']['first_name'], 'UpdatedName')

  def test_delete_user(self):
    url = f"{self.user_list_url}{self.normal_user.id}/"
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_non_admin_cannot_list_users(self):
    # Crear otro cliente con usuario normal
    self.client.credentials()  # Limpiar auth
    login_response = self.client.post(self.login_url, {
      'email': 'user@example.com',
      'password': 'UserPassword123'
    }, format='json')
    user_access_token = login_response.data['data']['access']
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

    response = self.client.get(self.user_list_url)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

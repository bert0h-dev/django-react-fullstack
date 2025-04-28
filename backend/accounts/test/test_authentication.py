from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AuthenticationTests(APITestCase):
  def setUp(self):
    self.login_url = reverse('login')
    self.logout_url = reverse('logout')
    self.user = User.objects.create_user(
      email='testuser@example.com',
      username='testuser',
      password='TestPassword123',
      first_name='Test',
      last_name='User',
      user_type='staff',
      is_verified=True,
      is_active=True
    )

  def test_login_successful(self):
    data = {
      'email': 'testuser@example.com',
      'password': 'TestPassword123'
    }
    response = self.client.post(self.login_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data['data'])
    self.assertIn('refresh', response.data['data'])
    self.assertIn('user', response.data['data'])
    self.assertEqual(response.data['data']['user']['email'], 'testuser@example.com')

  def test_login_invalid_credentials(self):
    data = {
      'email': 'testuser@example.com',
      'password': 'WrongPassword'
    }
    response = self.client.post(self.login_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_logout_successful(self):
    # Primero hacemos login para obtener tokens
    login_data = {
      'email': 'testuser@example.com',
      'password': 'TestPassword123'
    }
    login_response = self.client.post(self.login_url, login_data, format='json')
    refresh_token = login_response.data['data']['refresh']
    access_token = login_response.data['data']['access']

    # Ahora hacemos logout usando el refresh token
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    logout_data = {
      'refresh': refresh_token
    }
    response = self.client.post(self.logout_url, logout_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

  def test_logout_with_invalid_token(self):
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer faketoken123')
    logout_data = {
      'refresh': 'invalidtoken'
    }
    response = self.client.post(self.logout_url, logout_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RefreshTokenTests(APITestCase):
  def setUp(self):
    self.user = User.objects.create_user(
      email='refreshuser@example.com',
      username='refreshuser',
      password='RefreshPass123',
      first_name='Refresh',
      last_name='User',
      is_active=True
    )

    self.login_url = reverse('login')
    self.refresh_url = reverse('token_refresh')

    # Hacemos login para obtener los tokens
    login_response = self.client.post(self.login_url, {
      'email': 'refreshuser@example.com',
      'password': 'RefreshPass123'
    }, format='json')

    self.refresh_token = login_response.data['data']['refresh']
    self.access_token = login_response.data['data']['access']

  def test_refresh_token_successful(self):
    response = self.client.post(self.refresh_url, {'refresh': self.refresh_token}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data['data'])

  def test_refresh_token_missing(self):
    response = self.client.post(self.refresh_url, {}, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_refresh_token_invalid(self):
    response = self.client.post(self.refresh_url, {'refresh': 'invalidtoken'}, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

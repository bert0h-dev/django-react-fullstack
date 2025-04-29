# accounts/tests/test_change_password.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangePasswordTests(APITestCase):
  def setUp(self):
    self.admin_user = User.objects.create_user(
      email='admin@example.com',
      password='Admin123!',
      is_staff=True,
      is_superuser=True
    )
    self.target_user = User.objects.create_user(
      email='target@example.com',
      password='OldPassword123!'
    )

    self.client.force_authenticate(user=self.admin_user)

  def test_change_password_success(self):
    url = reverse('user_change_password', kwargs={'user_id': self.target_user.id})
    data = {
      "current_password": "OldPassword123!",
      "new_password": "NewPassword123!",
      "confirm_password": "NewPassword123!"
    }
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.target_user.refresh_from_db()
    self.assertTrue(self.target_user.check_password("NewPassword123!"))

  def test_change_password_mismatch(self):
    url = reverse('user_change_password', kwargs={'user_id': self.target_user.id})
    data = {
      "current_password": "OldPassword123!",
      "new_password": "NewPassword123!",
      "confirm_password": "OtherPassword123!"
    }
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('confirm_password', response.data)

  def test_change_password_weak(self):
    url = reverse('user_change_password', kwargs={'user_id': self.target_user.id})
    data = {
      "current_password": "OldPassword123!",
      "new_password": "weak",
      "confirm_password": "weak"
    }
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('new_password', response.data)

  def test_change_password_wrong_current_password(self):
    url = reverse('user_change_password', kwargs={'user_id': self.target_user.id})
    data = {
      "current_password": "WrongOldPassword!",
      "new_password": "NewPassword123!",
      "confirm_password": "NewPassword123!"
    }
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('current_password', response.data)

  def test_permission_denied_for_non_admin(self):
    non_admin = User.objects.create_user(
      email='user@example.com',
      password='User123!'
    )
    self.client.force_authenticate(user=non_admin)

    url = reverse('user_change_password', kwargs={'user_id': self.target_user.id})
    data = {
      "current_password": "OldPassword123!",
      "new_password": "ValidPass123!",
      "confirm_password": "ValidPass123!"
    }
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

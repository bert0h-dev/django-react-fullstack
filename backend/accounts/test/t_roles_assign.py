from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class AssignRoleTests(APITestCase):
  def setUp(self):
    self.admin = User.objects.create_user(
      email='admin@example.com',
      password='Admin123!',
      is_staff=True,
      is_superuser=True
    )

    self.user = User.objects.create_user(
      email='user@example.com',
      password='User123!'
    )

    self.other_user = User.objects.create_user(
      email='otheruser@example.com',
      password='OtherUser123!'
    )

    self.role = Group.objects.create(name="TestRole")

    self.client.force_authenticate(user=self.admin)

  def assign_role_url(self, user_id):
    return reverse('assign_user_role', kwargs={'user_id': user_id})

  def test_assign_role_success(self):
    data = {"role_id": self.role.id}
    response = self.client.post(self.assign_role_url(self.user.id), data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(self.role in self.user.groups.all())

  def test_assign_role_invalid_user(self):
    data = {"role_id": self.role.id}
    response = self.client.post(self.assign_role_url(9999), data)  # Usuario que no existe
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_assign_invalid_role(self):
    data = {"role_id": 9999}  # Rol que no existe
    response = self.client.post(self.assign_role_url(self.user.id), data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_only_admin_can_assign_role(self):
    self.client.force_authenticate(user=self.other_user)  # Ahora autenticamos un user normal
    data = {"role_id": self.role.id}
    response = self.client.post(self.assign_role_url(self.user.id), data)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

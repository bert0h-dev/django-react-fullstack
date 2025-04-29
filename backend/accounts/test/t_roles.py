from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()

class RoleViewSetTests(APITestCase):
  def setUp(self):
    # Creamos un admin para autenticarnos
    self.admin = User.objects.create_user(
      email='admin@example.com',
      password='Admin123!',
      is_staff=True,
      is_superuser=True
    )
    self.client.force_authenticate(user=self.admin)

    # Creamos un rol base
    self.role = Group.objects.create(name="TestRole")

    # URLs base
    self.roles_url = reverse('roles-list')  # Listar y crear
    self.role_detail_url = lambda pk: reverse('roles-detail', kwargs={'pk': pk})  # Detalle, update, destroy

  def test_list_roles(self):
    response = self.client.get(self.roles_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertGreaterEqual(len(response.data['results']), 1)

  def test_retrieve_role(self):
    response = self.client.get(self.role_detail_url(self.role.id))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], "TestRole")

  def test_create_role(self):
    data = {"name": "NewRole"}
    response = self.client.post(self.roles_url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['name'], "NewRole")

  def test_update_role(self):
    data = {"name": "UpdatedRole"}
    response = self.client.put(self.role_detail_url(self.role.id), data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], "UpdatedRole")

  def test_partial_update_role(self):
    data = {"name": "PartialUpdateRole"}
    response = self.client.patch(self.role_detail_url(self.role.id), data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], "PartialUpdateRole")

  def test_destroy_role_without_users(self):
    response = self.client.delete(self.role_detail_url(self.role.id))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertFalse(Group.objects.filter(id=self.role.id).exists())

  def test_destroy_role_with_users(self):
    # Asignamos el rol a un usuario
    user = User.objects.create_user(email='testuser@example.com', password='User123!')
    user.groups.add(self.role)

    response = self.client.delete(self.role_detail_url(self.role.id))
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertTrue(Group.objects.filter(id=self.role.id).exists())
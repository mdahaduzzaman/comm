from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Shop
from users.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

class ShopAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', password='testpassword', full_name="Test User", is_active=True)

        # Obtain JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.shop_data = {'name': 'Test Shop', 'owner': self.user.id, 'is_active': True}
        self.url = reverse('shop-list')

    def test_create_shop_as_admin_active_status_true(self):
        # Create a staff user
        admin_user = User.objects.create_user(email='admin@gmail.com', password='adminpassword', is_active=True, is_staff=True, full_name="Admin")
        self.client.force_authenticate(user=admin_user)

        shop_data = {"name": "Admin Shop", "owner": admin_user.id, 'is_active': True}

        response = self.client.post(self.url, shop_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_shop_as_non_admin(self):
        response = self.client.post(self.url, self.shop_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_shop(self):
        shop = Shop.objects.create(name='Shop 1', owner=self.user)
        response = self.client.get(reverse('shop-detail', kwargs={'pk': shop.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Shop 1')

    def test_update_active_status_not_possible_by_user(self):
        shop = Shop.objects.create(name='Shop 1', owner=self.user)
        updated_data = {'name': 'Updated Shop', 'owner': self.user.id, 'is_active': True}
        response = self.client.put(reverse('shop-detail', kwargs={'pk': shop.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_shop_active_status_as_admin(self):
        admin_user = User.objects.create_user(email='admin@gmail.com', password='adminpassword', is_staff=True)
        self.client.force_authenticate(user=admin_user)

        shop = Shop.objects.create(name='Shop 1', owner=admin_user, is_active=True)
        updated_data = {'name': 'Updated Shop', 'owner': admin_user.id, 'is_active': False}
        response = self.client.put(reverse('shop-detail', kwargs={'pk': shop.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_shop(self):
        shop = Shop.objects.create(name='Shop 1', owner=self.user)
        response = self.client.delete(reverse('shop-detail', kwargs={'pk': shop.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


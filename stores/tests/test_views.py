from django.urls import reverse
from rest_framework import status
from .test_setup import TestSetUp
from stores.models import Shop
from users.models import User
from rest_framework.test import APIClient


class ShopAPITestCase(TestSetUp):
    def test_not_authenticated_people_can_view_shop(self):
        """If the user is anonymous they can get all shop or not"""
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_shop_as_non_admin(self):
        """normal user can create a shop or not"""
        response = self.client.post(self.url, self.shop_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_shop(self):
        """retrive a shop or not"""
        shop = Shop.objects.create(name='Shop 1', owner=self.user)
        response = self.client.get(reverse('shops-detail', kwargs={'pk': shop.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Shop 1')

    def test_create_shop_as_admin_active_status_true(self):
        """staff user can create active shop or not"""
        admin_user = User.objects.create_user(email='admin@gmail.com', password='adminpassword', is_active=True, is_staff=True, full_name="Admin")
        self.client.force_authenticate(user=admin_user)
        shop_data = {"name": "Admin Shop", "owner": admin_user.id, 'is_active': True}
        response = self.client.post(self.url, shop_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_shop_active_status_as_admin(self):
        """admin can update shop active status or not"""
        admin_user = User.objects.create_user(email='admin@gmail.com', password='adminpassword', is_staff=True)
        self.client.force_authenticate(user=admin_user)
        shop = Shop.objects.create(name='Shop 1', owner=admin_user, is_active=False)
        updated_data = {'name': 'Updated Shop', 'owner': admin_user.id, 'is_active': True}
        response = self.client.put(reverse('shops-detail', kwargs={'pk': shop.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_active_status_not_possible_by_normal_user(self):
        shop = Shop.objects.create(name='Shop 1', owner=self.user)
        updated_data = {'name': 'Updated Shop', 'owner': self.user.id, 'is_active': True}
        response = self.client.put(reverse('shops-detail', kwargs={'pk': shop.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_shop_by_owner_user(self):
        shop = Shop.objects.create(name='Shop 1', owner=self.user)
        response = self.client.delete(reverse('shops-detail', kwargs={'pk': shop.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_shop_by_another_user_not_possible(self):
        new_user = User.objects.create(email="new@gmail.com", password="newuser", full_name="New User", is_active=True)
        shop1 = Shop.objects.create(name='Shop 1', owner=new_user)

        response = self.client.delete(reverse('shops-detail', kwargs={'pk': shop1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryAPITestCase(TestSetUp):
    def test_view_category_as_normal_user(self):
        client = APIClient()
        response = client.get(reverse('categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_as_normal_user(self):
        client = APIClient()
        image_path = "/home/ahaduzzaman/Desktop/ecommerce/media/Category/Image/Electronics__Computers_electronics.jpg"
        
        # Open the image file
        with open(image_path, "rb") as image_file:
            # Wrap the file object using Django's File class
            image_data = image_file
            
            # Create the payload with the wrapped file object
            valid_payload = {
                'name': 'Test Category',
                'category_image': image_data
            }

            response = client.post(reverse('categories-list'), valid_payload, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_as_authenticated_user(self):
        # Define the absolute path to the test image file
        test_image_path = "/home/ahaduzzaman/Desktop/ecommerce/media/Category/Image/Electronics__Computers_electronics.jpg"
        
        # Open the image file
        with open(test_image_path, "rb") as image_file:
            # Wrap the file object using Django's File class
            image_data = image_file
            
            # Create the payload with the wrapped file object
            valid_payload = {
                'name': 'Test Category',
                'category_image': image_data
            }
            
            response = self.client.post(reverse('categories-list'), valid_payload, format='multipart')
            
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


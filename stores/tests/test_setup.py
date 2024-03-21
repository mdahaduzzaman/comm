from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import os

class TestSetUp(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', password='testpassword', full_name="Test User", is_active=True)

        # Obtain JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.shop_data = {'name': 'Test Shop', 'owner': self.user.id, 'is_active': True}
        self.url = reverse('shops-list')
        return super().setUp()
    
    def tearDown(self):
        from django.core.files.storage import default_storage

        def delete_files(directory):
            # Correctly iterate over files and subdirectories:
            for entry in os.listdir(directory):
                file_path = os.path.join(directory, entry)
                if os.path.isdir(file_path):
                    # Recursively delete files within subdirectories:
                    delete_files(file_path)
                else:
                    # Delete files starting with 'Test':
                    if entry.startswith('Test'):
                        os.remove(file_path)

        # Specify the correct path to your media directory:
        media_root = settings.MEDIA_ROOT

        # Initiate deletion of files within the media directory:
        delete_files(media_root)
        return super().tearDown()
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from rest_framework import status

from io import BytesIO
from PIL import Image


CREATE_USER_URL = reverse('users:create')
JWT_URL = reverse('users:token')
PROFILE_URL = reverse('users:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_photo_file():
    data = BytesIO()
    Image.new('RGB', (100, 100)).save(data, 'PNG')
    data.seek(0)
    return SimpleUploadedFile('photo.png', data.getvalue())


class PublicUserApiTests(TestCase):
    """Test the users API (Public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        photo_file = create_photo_file()
        payload = {
            'email': 'id.purwowd@gmail.com',
            'password': 'pass123',
            'name': 'Test name',
            'photo': photo_file,
        }
        res = self.client.post(CREATE_USER_URL, payload)

        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(res.data['name'], user.name)
        self.assertEqual(res.data['email'], user.email)
        self.assertTrue(user.check_password(payload['password']))
        self.assertIsNotNone(user.photo)

    def test_user_exist(self):
        """Test creating a user that already exist fails"""
        payload = {'email': 'id.purwowd@gmail.com', 'password': 'pass123'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'id.purwowd@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_jwt_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'id.purwowd@gmail.com', 'password': 'pass123'}
        create_user(**payload)
        res = self.client.post(JWT_URL, payload)

        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_jwt_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='id.purwowd@gmail.com', password='pass123')
        payload = {'email': 'id.purwowd@gmail.com', 'password': 'gundulgundul'}
        res = self.client.post(JWT_URL, payload)

        self.assertNotIn('refresh', res.data)
        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_jwt_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'id.purwowd@gmail.com', 'password': 'pass123'}
        res = self.client.post(JWT_URL, payload)

        self.assertNotIn('refresh', res.data)
        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_jwt_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(JWT_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('refresh', res.data)
        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.user = create_user(
            email='id.purwowd@gmail.com',
            password='testpass',
            name='test',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
            'photo': None
        })

    def test_post_me_not_allowed(self):
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

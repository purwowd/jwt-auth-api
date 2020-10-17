from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """
        Test creating a new user with an email is successfull
        """
        email = 'id.purwowd@gmail.com'
        password = 'qwerty123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        email = 'id.purwowd@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email, 'qwerty123'
        )

        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """
        Test creating user with no email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'qwerty123')

    def create_new_superuser(self):
        """
        Test creating a new superuser
        """
        superuser = get_user_model().objects.create_superuser(
            'id.purwowd@gmail.com',
            'qwerty123'
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

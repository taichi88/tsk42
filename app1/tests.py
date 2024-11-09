# app1/tests.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from . import urls

class UserAuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()  # Create an instance of the test client
        self.register_url = '/register/'
        self.login_url = '/login/'
        self.logout_url = '/logout/'

    def test_register_user(self):
        # Test user registration
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user_successful(self):
        # Create user and test login with correct credentials
        User.objects.create_user(username='testuser', password='testpassword')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_invalid(self):
        # Test login with incorrect credentials
        data = {'username': 'wronguser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_user(self):
        # First log the user in, then test logout
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

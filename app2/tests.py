# app2/tests.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Car

class CarModelTest(TestCase):

    def setUp(self):
        # Create a user for the foreign key relationship
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_car_creation(self):
        # Create a car instance and check its fields
        car = Car.objects.create(
            make="Toyota",
            model="Camry",
            year_model=2022,
            price=25000.00,
            user=self.user
        )
        self.assertEqual(car.make, "Toyota")
        self.assertEqual(car.model, "Camry")
        self.assertEqual(car.year_model, 2022)
        self.assertEqual(car.price, 25000.00)

    def test_car_price_validation(self):
        # Create a car instance and validate the price field
        car = Car.objects.create(
            make="Honda",
            model="Civic",
            year_model=2021,
            price=10000.00,
            user=self.user
        )
        self.assertTrue(car.price > 0)

class CarViewsTest(TestCase):

    def setUp(self):
        # Set up test client and create a user and car instance
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.create_url = '/'
        self.car = Car.objects.create(
            make='Toyota',
            model='Camry',
            year_model=2022,
            price=25000.00,
            user=self.user
        )

    def test_create_car(self):
        # Test creating a new car
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'year_model': 2021,
            'price': 22000.00,
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_cars(self):
        # Test retrieving the list of cars for the logged-in user
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # There should be at least one car

    def test_get_car(self):
        # Test retrieving a single car by its ID
        response = self.client.get(f'/{self.car.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['make'], 'Toyota')

    def test_update_car(self):
        # Test updating an existing car
        data = {
            'make': 'Honda',
            'model': 'Accord',
            'year_model': 2020,
            'price': 24000.00,
        }
        response = self.client.patch(f'/{self.car.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_car(self):
        # Test deleting an existing car
        response = self.client.delete(f'/{self.car.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

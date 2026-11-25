
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class AccountTests(APITestCase):

    def test_user_can_register(self):
        response = self.client.post(
            '/api/accounts/register/',
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'TestPassword123!',
                'password2': 'TestPassword123!',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='testuser')

        self.assertTrue(
            user.check_password('TestPassword123!')
        )

        self.assertNotIn('password', response.data)

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(
            '/api/accounts/register/',
            {
                'username': 'anotheruser',
                'email': 'another@example.com',
                'password': 'TestPassword123!',
                'password2': 'DifferentPassword123!',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_cannot_access_profile(self):
        response = self.client.get('/api/accounts/profile/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_profile(self):
        user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='TestPassword123!'
        )

        self.client.force_authenticate(user=user)

        response = self.client.get('/api/accounts/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profileuser')
        self.assertEqual(response.data['email'], 'profile@example.com')


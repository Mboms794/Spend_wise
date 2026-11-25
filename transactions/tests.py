
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import User
from transactions.models import Transaction


class TransactionAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='transaction_user',
            email='transaction@example.com',
            password='TestPassword123!'
        )

        self.client.force_authenticate(user=self.user)

        self.url = reverse('transaction-list-create')

    def test_user_can_create_transaction(self):
        data = {
            'title': 'Lunch',
            'amount': '5000.00',
            'transaction_type': 'expense',
            'category': 'food',
            'description': 'Lunch payment',
            'date': '2026-11-24',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.title, 'Lunch')

    def test_unauthenticated_user_cannot_access_transactions(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_transaction_rejects_invalid_amount(self):
        for amount in ['0.00', '-100.00']:
            with self.subTest(amount=amount):
                data = {
                    'title': 'Invalid transaction',
                    'amount': amount,
                    'transaction_type': 'expense',
                    'category': 'food',
                    'description': 'Testing invalid amount',
                    'date': '2026-11-24',
                }

                response = self.client.post(
                    self.url,
                    data,
                    format='json'
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST
                )

        self.assertEqual(Transaction.objects.count(), 0)

    def test_user_can_only_see_own_transactions(self):
        Transaction.objects.create(
            user=self.user,
            title='My Lunch',
            amount='5000.00',
            transaction_type='expense',
            category='food',
            date='2026-11-24'
        )

        another_user = User.objects.create_user(
            username='another_user',
            email='another@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_access_another_users_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            title='Private Lunch',
            amount='5000.00',
            transaction_type='expense',
            category='food',
            date='2026-11-24'
        )

        another_user = User.objects.create_user(
            username='another_user',
            email='another@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        detail_url = reverse(
            'transaction-detail',
            kwargs={'pk': transaction.pk}
        )

        response = self.client.get(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_user_can_retrieve_own_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            title='My Lunch',
            amount='5000.00',
            transaction_type='expense',
            category='food',
            date='2026-11-24'
        )

        detail_url = reverse(
            'transaction-detail',
            kwargs={'pk': transaction.pk}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'My Lunch')

    def test_user_can_update_own_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            title='Old Lunch',
            amount='5000.00',
            transaction_type='expense',
            category='food',
            date='2026-11-24'
        )

        detail_url = reverse(
            'transaction-detail',
            kwargs={'pk': transaction.pk}
        )

        response = self.client.patch(
            detail_url,
            {'title': 'Updated Lunch'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        transaction.refresh_from_db()
        self.assertEqual(transaction.title, 'Updated Lunch')

    def test_user_can_delete_own_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            title='Lunch to Delete',
            amount='5000.00',
            transaction_type='expense',
            category='food',
            date='2026-11-24'
        )

        detail_url = reverse(
            'transaction-detail',
            kwargs={'pk': transaction.pk}
        )

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Transaction.objects.filter(pk=transaction.pk).exists()
        )

    def test_user_cannot_update_or_delete_another_users_transaction(self):
        transaction = Transaction.objects.create(
            user=self.user,
            title='Private Transaction',
            amount='5000.00',
            transaction_type='expense',
            category='food',
            date='2026-11-24'
        )

        another_user = User.objects.create_user(
            username='another_user',
            email='another@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        detail_url = reverse(
            'transaction-detail',
            kwargs={'pk': transaction.pk}
        )

        update_response = self.client.patch(
            detail_url,
            {'title': 'Unauthorized Update'},
            format='json'
        )

        delete_response = self.client.delete(detail_url)

        self.assertEqual(
            update_response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            delete_response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertTrue(
            Transaction.objects.filter(pk=transaction.pk).exists()
        )


from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from budgets.models import Budget
from transactions.models import Transaction


class BudgetAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='budget_user',
            email='budget@example.com',
            password='TestPassword123!'
        )

        self.client.force_authenticate(user=self.user)

        self.url = reverse('budget-list-create')

    def create_budget(self, **overrides):
        data = {
            'name': 'Food Budget',
            'category': 'food',
            'limit_amount': '50000.00',
            'period': 'monthly',
            'start_date': '2026-11-01',
            'end_date': '2026-11-30',
        }
        data.update(overrides)

        return Budget.objects.create(
            user=self.user,
            **data
        )

    def test_user_can_create_budget(self):
        data = {
            'name': 'Food Budget',
            'category': 'food',
            'limit_amount': '50000.00',
            'period': 'monthly',
            'start_date': '2026-11-01',
            'end_date': '2026-11-30',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)

        budget = Budget.objects.first()
        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.name, 'Food Budget')

    def test_unauthenticated_user_cannot_access_budgets(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_budget_rejects_zero_and_negative_amounts(self):
        for amount in ['0.00', '-100.00']:
            with self.subTest(amount=amount):
                data = {
                    'name': 'Invalid Budget',
                    'category': 'food',
                    'limit_amount': amount,
                    'period': 'monthly',
                    'start_date': '2026-11-01',
                    'end_date': '2026-11-30',
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

        self.assertEqual(Budget.objects.count(), 0)

    def test_budget_rejects_end_date_before_start_date(self):
        data = {
            'name': 'Invalid Dates',
            'category': 'food',
            'limit_amount': '50000.00',
            'period': 'monthly',
            'start_date': '2026-11-20',
            'end_date': '2026-11-10',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(Budget.objects.count(), 0)

    def test_user_cannot_create_overlapping_budget_for_same_category(self):
        self.create_budget()

        data = {
            'name': 'Another Food Budget',
            'category': 'food',
            'limit_amount': '30000.00',
            'period': 'monthly',
            'start_date': '2026-11-15',
            'end_date': '2026-12-15',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(Budget.objects.count(), 1)

    def test_user_can_create_budget_for_different_category(self):
        self.create_budget()

        data = {
            'name': 'Transport Budget',
            'category': 'transportation',
            'limit_amount': '20000.00',
            'period': 'monthly',
            'start_date': '2026-11-01',
            'end_date': '2026-11-30',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 2)

    def test_user_can_only_see_own_budgets(self):
        self.create_budget()

        another_user = User.objects.create_user(
            username='another_budget_user',
            email='anotherbudget@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_access_another_users_budget(self):
        budget = self.create_budget()

        another_user = User.objects.create_user(
            username='another_budget_user',
            email='anotherbudget@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        detail_url = reverse(
            'budget-detail',
            kwargs={'pk': budget.pk}
        )

        response = self.client.get(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_user_can_update_own_budget(self):
        budget = self.create_budget()

        detail_url = reverse(
            'budget-detail',
            kwargs={'pk': budget.pk}
        )

        response = self.client.patch(
            detail_url,
            {'limit_amount': '75000.00'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        budget.refresh_from_db()
        self.assertEqual(budget.limit_amount, Decimal('75000.00'))

    def test_user_can_delete_own_budget(self):
        budget = self.create_budget()

        detail_url = reverse(
            'budget-detail',
            kwargs={'pk': budget.pk}
        )

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Budget.objects.filter(pk=budget.pk).exists()
        )

    def test_budget_spending_calculations(self):
        budget = self.create_budget()

        Transaction.objects.create(
            user=self.user,
            title='Food Shopping',
            amount=Decimal('20000.00'),
            transaction_type='expense',
            category='food',
            date='2026-11-10'
        )

        Transaction.objects.create(
            user=self.user,
            title='More Food',
            amount=Decimal('10000.00'),
            transaction_type='expense',
            category='food',
            date='2026-11-15'
        )

        detail_url = reverse(
            'budget-detail',
            kwargs={'pk': budget.pk}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Decimal(str(response.data['spent_amount'])),
            Decimal('30000.00')
        )
        self.assertEqual(
            Decimal(str(response.data['remaining_amount'])),
            Decimal('20000.00')
        )
        self.assertEqual(
            Decimal(str(response.data['percentage_used'])),
            Decimal('60.00')
        )
        self.assertEqual(response.data['budget_status'], 'normal')


from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from budgets.models import Budget
from transactions.models import Transaction


class BudgetInsightTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='ai_test_user',
            email='ai_test@example.com',
            password='TestPassword123!'
        )

        self.other_user = User.objects.create_user(
            username='other_ai_user',
            email='other_ai@example.com',
            password='TestPassword123!'
        )

        self.today = timezone.localdate()

        self.budget = Budget.objects.create(
            user=self.user,
            name='Food Budget',
            category='food',
            limit_amount=Decimal('100000.00'),
            period='monthly',
            start_date=self.today - timedelta(days=10),
            end_date=self.today + timedelta(days=20)
        )

        self.url = f'/api/ai/budget-insight/{self.budget.id}/'

    def create_expense(self, amount):
        return Transaction.objects.create(
            user=self.user,
            title='Food Expense',
            amount=Decimal(str(amount)),
            transaction_type='expense',
            category='food',
            date=self.today
        )

    def test_unauthenticated_user_cannot_access_insight(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_user_can_access_own_budget_insight(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['budget_name'],
            'Food Budget'
        )

    def test_user_cannot_access_another_users_budget(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_normal_budget_insight(self):
        self.client.force_authenticate(user=self.user)

        self.create_expense('30000.00')

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['budget_status'],
            'normal'
        )
        self.assertIn(
            'within its limit',
            response.data['explanation']
        )
        self.assertIn(
            'recommendation',
            response.data
        )

    def test_warning_budget_insight(self):
        self.client.force_authenticate(user=self.user)

        self.create_expense('85000.00')

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['budget_status'],
            'warning'
        )
        self.assertIn(
            'approaching its limit',
            response.data['explanation']
        )

    def test_exceeded_budget_insight(self):
        self.client.force_authenticate(user=self.user)

        self.create_expense('120000.00')

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['budget_status'],
            'exceeded'
        )
        self.assertIn(
            'exceeded',
            response.data['explanation']
        )

    def test_insight_response_contains_expected_fields(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        expected_fields = [
            'budget_name',
            'spent_amount',
            'limit_amount',
            'remaining_amount',
            'percentage_used',
            'budget_status',
            'explanation',
            'recommendation',
        ]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        for field in expected_fields:
            self.assertIn(field, response.data)

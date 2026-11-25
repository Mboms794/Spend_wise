
from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from transactions.models import Transaction
from reports.services import generate_spending_analysis


class SpendingAnalysisTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='reports_user',
            email='reports@example.com',
            password='TestPassword123!'
        )
        self.today = timezone.localdate()

    def create_transaction(
        self,
        title,
        amount,
        category='food',
        transaction_type='expense',
        date=None,
        user=None
    ):
        return Transaction.objects.create(
            user=user or self.user,
            title=title,
            amount=Decimal(str(amount)),
            category=category,
            transaction_type=transaction_type,
            date=date or self.today
        )

    def test_spending_analysis_calculates_total_and_count(self):
        self.create_transaction('Food', '20000')
        self.create_transaction('Transport', '10000')

        result = generate_spending_analysis(
            self.user,
            self.today - timedelta(days=10),
            self.today
        )

        self.assertEqual(result['total_spent'], '30000')
        self.assertEqual(result['transaction_count'], 2)

    def test_spending_analysis_calculates_average_daily_spending(self):
        self.create_transaction('Food', '20000')

        result = generate_spending_analysis(
            self.user,
            self.today - timedelta(days=9),
            self.today
        )

        self.assertEqual(result['average_daily_spending'], '2000.00')

    def test_spending_analysis_identifies_largest_expense(self):
        self.create_transaction('Laptop Purchase', '80000')
        self.create_transaction('Small Purchase', '5000')

        result = generate_spending_analysis(
            self.user,
            self.today - timedelta(days=10),
            self.today
        )

        self.assertEqual(
            result['largest_expense']['title'],
            'Laptop Purchase'
        )
        self.assertEqual(
            result['largest_expense']['amount'],
            '80000.00'
        )

    def test_spending_analysis_groups_transactions_by_category(self):
        self.create_transaction('Food 1', '10000', category='food')
        self.create_transaction('Food 2', '15000', category='food')
        self.create_transaction(
            'Transport',
            '5000',
            category='transportation'
        )

        result = generate_spending_analysis(
            self.user,
            self.today - timedelta(days=10),
            self.today
        )

        food_category = next(
            category for category in result['categories']
            if category['category'] == 'food'
        )

        self.assertEqual(food_category['total_spent'], '25000')
        self.assertEqual(food_category['transaction_count'], 2)
        self.assertEqual(
            result['highest_spending_category'],
            'food'
        )

    def test_spending_analysis_compares_previous_period(self):
        start_date = self.today - timedelta(days=9)
        previous_start = start_date - timedelta(days=10)

        self.create_transaction(
            'Previous Spending',
            '10000',
            date=previous_start
        )
        self.create_transaction(
            'Current Spending',
            '20000',
            date=start_date
        )

        result = generate_spending_analysis(
            self.user,
            start_date,
            self.today
        )

        self.assertEqual(result['spending_change'], '10000')
        self.assertEqual(result['percentage_change'], '100.00')
        self.assertEqual(result['spending_trend'], 'increased')

    def test_spending_analysis_excludes_income_and_other_users(self):
        another_user = User.objects.create_user(
            username='another_user',
            email='another@example.com',
            password='TestPassword123!'
        )

        self.create_transaction(
            'My Expense',
            '10000'
        )
        self.create_transaction(
            'My Income',
            '50000',
            transaction_type='income'
        )
        self.create_transaction(
            'Other User Expense',
            '30000',
            user=another_user
        )

        result = generate_spending_analysis(
            self.user,
            self.today - timedelta(days=10),
            self.today
        )

        self.assertEqual(result['total_spent'], '10000')
        self.assertEqual(result['transaction_count'], 1)

    def test_spending_analysis_handles_no_transactions(self):
        result = generate_spending_analysis(self.user)

        self.assertEqual(result['total_spent'], '0.00')
        self.assertEqual(result['transaction_count'], 0)
        self.assertIsNone(result['largest_expense'])
        self.assertIsNone(result['highest_spending_category'])
        self.assertEqual(result['spending_trend'], 'unchanged')
        self.assertEqual(result['percentage_change'], '0.00')

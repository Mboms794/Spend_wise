
from decimal import Decimal
from datetime import timedelta

from django.db.models import Sum, Count
from django.utils import timezone

from transactions.models import Transaction

def generate_spending_analysis(user, start_date=None, end_date=None):
    today = timezone.localdate()

    if start_date is None and end_date is None:
        end_date = today
        start_date = today - timedelta(days=29)
    transactions = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__range=(start_date, end_date)
    )
    # Current period summary
    summary = transactions.aggregate(
        total=Sum('amount'),
        count=Count('id')
    )

    total_spent = summary['total'] or Decimal('0.00')
    transaction_count = summary['count']

   # Previous period of equal length
    period_days = (end_date - start_date).days + 1

    previous_end_date = start_date - timedelta(days=1)

    previous_start_date = (
        previous_end_date - timedelta(days=period_days - 1)
    )

    previous_transactions = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__range=(previous_start_date, previous_end_date)
    )

    previous_total_spent = (
        previous_transactions.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
    )

    # Spending comparison
    spending_change = total_spent - previous_total_spent

    if previous_total_spent > 0:
        percentage_change = (
            spending_change / previous_total_spent
            * Decimal('100')
        ).quantize(Decimal('0.01'))
    elif total_spent > 0:
        percentage_change = None
    else:
        percentage_change = Decimal('0.00')

    if spending_change > 0:
        spending_trend = 'increased'
    elif spending_change < 0:
        spending_trend = 'decreased'
    else:
        spending_trend = 'unchanged'
    average_daily_spending = (
        total_spent / Decimal(period_days)
    ).quantize(Decimal('0.01'))

    # Largest expense
    largest_expense = transactions.order_by('-amount').first()

    largest_expense_data = None

    if largest_expense:
        largest_expense_data = {
            'title': largest_expense.title,
            'amount': str(largest_expense.amount),
            'category': largest_expense.category,
            'date': str(largest_expense.date)
        }

    # Spending by category
    category_data = transactions.values(
        'category'
    ).annotate(
        total_spent=Sum('amount'),
        transaction_count=Count('id')
    ).order_by('-total_spent')

    categories = []

    for item in category_data:
        percentage = (
            (item['total_spent'] / total_spent) * Decimal('100')
            if total_spent > 0
            else Decimal('0.00')
        )

        categories.append({
            'category': item['category'],
            'total_spent': str(item['total_spent']),
            'transaction_count': item['transaction_count'],
            'percentage': str(
                percentage.quantize(Decimal('0.01'))
            )
        })

    highest_category = (
        categories[0]['category'] if categories else None
    )

    # Weekly spending breakdown
    weekly_data = {}

    for transaction in transactions.order_by('date'):
        week_start = (
            transaction.date
            - timedelta(days=transaction.date.weekday())
        )

        week_end = week_start + timedelta(days=6)
        week_label = f"{week_start} to {week_end}"

        weekly_data[week_label] = (
            weekly_data.get(
                week_label,
                Decimal('0.00')
            ) + transaction.amount
        )

    weekly_breakdown = [
        {
            'week': week,
            'total_spent': str(amount)
        }
        for week, amount in weekly_data.items()
    ]

    return {
        'period': (
        'Last 30 days'
        if period_days == 30 and end_date == today
        else 'Custom date range'
    ),
        'start_date': str(start_date),
        'end_date': str(end_date),
        'total_spent': str(total_spent),
        'transaction_count': transaction_count,
        'average_daily_spending': str(average_daily_spending),
        'largest_expense': largest_expense_data,
        'highest_spending_category': highest_category,
        'categories': categories,
        'weekly_breakdown': weekly_breakdown,
        'previous_period': {
            'start_date': str(previous_start_date),
            'end_date': str(previous_end_date),
            'total_spent': str(previous_total_spent)
        },
        'spending_change': str(spending_change),
        'percentage_change': (
            str(percentage_change)
            if percentage_change is not None
            else None
        ),
        'spending_trend': spending_trend
    }

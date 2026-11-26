from django.db import models
from django.conf import settings
from events.models import Event
from django.core.validators import MinValueValidator
from decimal import Decimal


class Transaction(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )

    title = models.CharField(max_length=200)

    amount = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.01'))]
)
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    CATEGORIES = [
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('housing', 'Housing'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('salary', 'Salary'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORIES
    )

    description = models.TextField(blank=True)

    date = models.DateField()
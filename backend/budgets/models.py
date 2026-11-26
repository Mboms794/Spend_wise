
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Budget(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets'
    )

    name = models.CharField(max_length=100)

    CATEGORIES = [
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('housing', 'Housing'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORIES
        )
    limit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]   

    period = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

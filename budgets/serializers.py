
from decimal import Decimal

from django.db.models import Sum
from rest_framework import serializers

from .models import Budget
from transactions.models import Transaction


class BudgetSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()
    budget_status = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            'id',
            'name',
            'category',
            'limit_amount',
            'period',
            'start_date',
            'end_date',
            'created_at',
            'spent_amount',
            'remaining_amount',
            'percentage_used',
            'budget_status',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'spent_amount',
            'remaining_amount',
            'percentage_used',
            'budget_status',
        ]

    def validate(self, attrs):
        start_date = attrs.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )

        end_date = attrs.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )

        category = attrs.get(
            'category',
            getattr(self.instance, 'category', None)
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                "End date cannot be earlier than start date."
            )

        if start_date and end_date and category:
            overlapping_budgets = Budget.objects.filter(
                user=self.context['request'].user,
                category=category,
                start_date__lte=end_date,
                end_date__gte=start_date
            )

            if self.instance:
                overlapping_budgets = overlapping_budgets.exclude(
                    pk=self.instance.pk
                )

            if overlapping_budgets.exists():
                raise serializers.ValidationError(
                    "You already have a budget for this category "
                    "covering some or all of these dates."
                )

        return attrs

    def calculate_spent(self, obj):
        if not hasattr(obj, '_spent_amount_cache'):
            result = Transaction.objects.filter(
                user=obj.user,
                transaction_type='expense',
                category=obj.category,
                date__range=(obj.start_date, obj.end_date)
            ).aggregate(total=Sum('amount'))

            obj._spent_amount_cache = (
                result['total'] or Decimal('0.00')
            )

        return obj._spent_amount_cache

    def get_spent_amount(self, obj) -> Decimal:
        return self.calculate_spent(obj)

    def get_remaining_amount(self, obj) -> Decimal:
        return obj.limit_amount - self.calculate_spent(obj)

    def get_percentage_used(self, obj) -> Decimal:
        percentage = (
            self.calculate_spent(obj) / obj.limit_amount
        ) * Decimal('100')

        return percentage.quantize(Decimal('0.01'))

    def get_budget_status(self, obj) -> str:
        percentage = self.get_percentage_used(obj)

        if percentage >= Decimal('100'):
            return 'exceeded'
        elif percentage >= Decimal('80'):
            return 'warning'

        return 'normal'


from decimal import Decimal

from django.db.models import Sum
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):

    total_spent = serializers.SerializerMethodField()
    remaining_budget = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'description',
            'budget',
            'event_date',
            'total_spent',
            'remaining_budget',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'id',
            'total_spent',
            'remaining_budget',
            'created_at',
            'updated_at'
        ]

    def get_total_spent(self, obj) -> Decimal:
        total = obj.transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total']

        return total if total is not None else Decimal('0.00')

    def get_remaining_budget(self, obj) -> Decimal:
        return obj.budget - self.get_total_spent(obj)

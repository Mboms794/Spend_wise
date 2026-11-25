
from rest_framework import serializers
from .models import Transaction
from events.models import Event


class TransactionSerializer(serializers.ModelSerializer):

    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'title',
            'amount',
            'transaction_type',
            'category',
            'description',
            'date',
            'event',
        ]

        read_only_fields = ['id']

    def validate_event(self, value):
        if value is not None and value.user != self.context['request'].user:
            raise serializers.ValidationError(
                "You can only attach a transaction to your own event."
            )

        return value

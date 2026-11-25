
from rest_framework import serializers


class LargestExpenseSerializer(serializers.Serializer):
    title = serializers.CharField()
    amount = serializers.CharField()
    category = serializers.CharField()
    date = serializers.CharField()


class CategorySpendingSerializer(serializers.Serializer):
    category = serializers.CharField()
    total_spent = serializers.CharField()
    transaction_count = serializers.IntegerField()
    percentage = serializers.CharField()


class WeeklySpendingSerializer(serializers.Serializer):
    week = serializers.CharField()
    total_spent = serializers.CharField()


class PreviousPeriodSerializer(serializers.Serializer):
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    total_spent = serializers.CharField()


class SpendingAnalysisSerializer(serializers.Serializer):
    period = serializers.CharField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    total_spent = serializers.CharField()
    transaction_count = serializers.IntegerField()
    average_daily_spending = serializers.CharField()

    largest_expense = LargestExpenseSerializer(
        allow_null=True
    )

    highest_spending_category = serializers.CharField(
        allow_null=True
    )

    categories = CategorySpendingSerializer(many=True)

    weekly_breakdown = WeeklySpendingSerializer(many=True)

    previous_period = PreviousPeriodSerializer()

    spending_change = serializers.CharField()

    percentage_change = serializers.CharField(
        allow_null=True
    )

    spending_trend = serializers.CharField()

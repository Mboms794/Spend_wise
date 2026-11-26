
from decimal import Decimal
from datetime import timedelta

from django.db.models import Sum, Count
from django.utils import timezone

from transactions.models import Transaction


def generate_budget_insight(budget_data):
    spent = Decimal(str(budget_data["spent_amount"]))
    limit = Decimal(str(budget_data["limit_amount"]))
    remaining = Decimal(str(budget_data["remaining_amount"]))
    percentage = Decimal(str(budget_data["percentage_used"]))
    status = budget_data["budget_status"]

    if status == "exceeded":
        explanation = (
            f"You have exceeded your {budget_data['name']}. "
            f"You have spent {percentage}% of your budget."
        )
        recommendation = (
            "Review your recent expenses and consider "
            "adjusting your spending or budget."
        )

    elif status == "warning":
        explanation = (
            f"Your {budget_data['name']} is approaching its limit. "
            f"You have used {percentage}% of your budget."
        )
        recommendation = (
            "Monitor your remaining expenses to avoid "
            "exceeding your budget."
        )

    else:
        explanation = (
            f"Your {budget_data['name']} is within its limit. "
            f"You have used {percentage}% of your budget."
        )
        recommendation = (
            "Continue monitoring your expenses "
            "to stay within your budget."
        )

    return {
        "budget_name": budget_data["name"],
        "spent_amount": str(spent),
        "limit_amount": str(limit),
        "remaining_amount": str(remaining),
        "percentage_used": str(percentage),
        "budget_status": status,
        "explanation": explanation,
        "recommendation": recommendation,
    }

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from budgets.models import Budget
from budgets.serializers import BudgetSerializer

from .services import generate_budget_insight
from drf_spectacular.utils import extend_schema


class BudgetInsightView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get AI budget insight",
        description="Returns an insight and recommendation for the authenticated user's budget.",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'budget_name': {'type': 'string'},
                    'spent_amount': {'type': 'string'},
                    'limit_amount': {'type': 'string'},
                    'remaining_amount': {'type': 'string'},
                    'percentage_used': {'type': 'string'},
                    'budget_status': {'type': 'string'},
                    'explanation': {'type': 'string'},
                    'recommendation': {'type': 'string'},
                },
            },
        },
    )
    def get(self, request, pk):
        budget = get_object_or_404(
            Budget,
            pk=pk,
            user=request.user
        )

        budget_data = BudgetSerializer(budget).data
        insight = generate_budget_insight(budget_data)

        return Response(insight)

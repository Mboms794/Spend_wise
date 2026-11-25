
from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .services import generate_spending_analysis
from .serializers import SpendingAnalysisSerializer


class SpendingAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get spending analysis",
        description=(
            "Returns spending analysis for the authenticated user. "
            "Provide both dates together in YYYY-MM-DD format."
        ),
        parameters=[
            OpenApiParameter(
                name="start_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Beginning of the reporting period.",
            ),
            OpenApiParameter(
                name="end_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                required=False,
                description="End of the reporting period.",
            ),
        ],
        responses={200: SpendingAnalysisSerializer},
    )
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Both dates must be provided together
        if bool(start_date) != bool(end_date):
            return Response(
                {
                    'error': 'Please provide both start_date and end_date.'
                },
                status=400
            )

        # Validate date format
        if start_date and end_date:
            try:
                start_date = date.fromisoformat(start_date)
                end_date = date.fromisoformat(end_date)
            except ValueError:
                return Response(
                    {
                        'error': 'Invalid date format. Use YYYY-MM-DD.'
                    },
                    status=400
                )

            # Validate date order
            if start_date > end_date:
                return Response(
                    {
                        'error': 'start_date cannot be later than end_date.'
                    },
                    status=400
                )

            if end_date > date.today():
                return Response(
                    {
                        'error': 'end_date cannot be in the future.'
                    },
                    status=400
                )

        analysis = generate_spending_analysis(
            request.user,
            start_date,
            end_date
        )

        return Response(analysis)

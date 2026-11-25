from django.urls import path

from .views import SpendingAnalysisView


urlpatterns = [
    path(
        'spending-analysis/',
        SpendingAnalysisView.as_view(),
        name='spending-analysis'
    ),
]
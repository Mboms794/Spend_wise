from django.urls import path

from .views import BudgetInsightView


urlpatterns = [
    path(
        'budget-insight/<int:pk>/',
        BudgetInsightView.as_view(),
        name='budget-insight'
    ),
]
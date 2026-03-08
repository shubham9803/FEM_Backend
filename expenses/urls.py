from django.urls import path
from .views import ExpenseCreateView, FamilyExpenseListView

urlpatterns = [
    path('create/', ExpenseCreateView.as_view(), name='create-expense'),
    path('list/', FamilyExpenseListView.as_view(), name='list-expense'),
]
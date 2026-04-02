from django.urls import path
from .views import ExpenseCreateView, FamilyExpenseListView,ExpenseDetailView

urlpatterns = [
    path('create/', ExpenseCreateView.as_view(), name='create-expense'),
    path('list/', FamilyExpenseListView.as_view(), name='list-expense'),

    # NEW: Endpoint for edit and delete
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
]
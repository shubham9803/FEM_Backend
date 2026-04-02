from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer
from datetime import date
from django.utils.timezone import now



class ExpenseCreateView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class FamilyExpenseListView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(family=user.family)

        # Get query params
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        # If not provided → use current month
        today = now().date()
        if not month:
            month = today.month
        if not year:
            year = today.year

        # Filter by month & year
        queryset = queryset.filter(
            expense_date__month=month,
            expense_date__year=year
        ).order_by('-expense_date')

        return queryset
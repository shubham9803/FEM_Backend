from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseCreateView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class FamilyExpenseListView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(family=user.family).order_by('-expense_date')
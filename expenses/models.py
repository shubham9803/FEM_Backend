from django.db import models
from django.conf import settings


class ExpenseCategory(models.TextChoices):
    CLOTHING = "CLOTHING", "Clothing"
    KITCHEN = "KITCHEN", "Kitchen Shopping"
    VEGETABLES = "VEGETABLES", "Vegetables"
    ELECTRONICS = "ELECTRONICS", "Electronics"
    RENT = "RENT", "Rent"
    DINING_OUT = "DINING_OUT", "Dining Out"
    GROCERIES = "GROCERIES", "Groceries"
    MEDICAL = "MEDICAL", "Medical"
    TRAVEL = "TRAVEL", "Travel"
    EDUCATION = "EDUCATION", "Education"
    ENTERTAINMENT = "ENTERTAINMENT", "Entertainment"
    UTILITIES = "UTILITIES", "Electricity/Water/Gas"
    FUEL = "FUEL", "Fuel"
    INTERNET = "INTERNET", "Internet"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    OTHER = "OTHER", "Other"
    


class PaymentMode(models.TextChoices):
    CASH = "CASH", "Cash"
    UPI = "UPI", "UPI"
    CARD = "CARD", "Card"
    NETBANKING = "NETBANKING", "Net Banking"


class Expense(models.Model):
    family = models.ForeignKey(
        'accounts.Family',   # Replace with actual app name
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses_added"
    )

    category = models.CharField(
        max_length=50,
        choices=ExpenseCategory.choices
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(blank=True, null=True)

    payment_mode = models.CharField(
        max_length=20,
        choices=PaymentMode.choices,
        default=PaymentMode.CASH
    )

    expense_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.family.name} - {self.category} - ₹{self.amount}"
from django.contrib import admin
from django.db.models import Sum
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    
    # ================================
    # LIST VIEW CONFIGURATION
    # ================================
    
    list_display = (
        "family",
        "category",
        "amount",
        "payment_mode",
        "expense_date",
        "added_by",
        "created_at",
    )

    list_filter = (
        "category",
        "payment_mode",
        "expense_date",
        "created_at",
        "family",
    )

    search_fields = (
        "description",
        "family__name",
        "added_by__username",
    )

    ordering = ("-expense_date",)

    date_hierarchy = "expense_date"

    list_per_page = 20

    list_editable = ("category", "payment_mode")

    autocomplete_fields = ("family", "added_by")

    readonly_fields = ("created_at",)

    # ================================
    # FIELD GROUPING (Clean UI)
    # ================================
    
    fieldsets = (
        ("Basic Information", {
            "fields": (
                "family",
                "added_by",
                "category",
                "amount",
                "description",
            )
        }),
        ("Payment Details", {
            "fields": (
                "payment_mode",
                "expense_date",
            )
        }),
        ("System Info", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    # ================================
    # PERFORMANCE OPTIMIZATION
    # ================================
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("family", "added_by")

    # ================================
    # SHOW TOTAL AMOUNT IN LIST VIEW
    # ================================
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data["cl"].queryset
            total = qs.aggregate(total_amount=Sum("amount"))["total_amount"] or 0
            response.context_data["total_amount"] = total
        except:
            pass
        return response

    # ================================
    # CUSTOM ACTION
    # ================================
    
    actions = ["mark_as_cash"]

    def mark_as_cash(self, request, queryset):
        updated = queryset.update(payment_mode="CASH")
        self.message_user(request, f"{updated} expenses marked as Cash.")
    mark_as_cash.short_description = "Mark selected expenses as Cash"
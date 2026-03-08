from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.utils.html import format_html

from .models import User, Family


# ============================================
# INLINE: Show Family Members Inside Family
# ============================================

class FamilyMemberInline(admin.TabularInline):
    model = User
    extra = 0
    fields = ("mobile", "fname", "lname", "email", "is_active")
    readonly_fields = ("mobile", "email")
    show_change_link = True


# ============================================
# FAMILY ADMIN
# ============================================

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "created_by",
        "member_count",
    )

    search_fields = (
        "name",
        "code",
        "created_by__mobile",
    )

    list_filter = (
        "created_by",
    )

    ordering = ("-id",)

    readonly_fields = ("code",)

    autocomplete_fields = ("created_by",)

    inlines = [FamilyMemberInline]

    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("created_by").annotate(
            _member_count=Count("members")
        )

    def member_count(self, obj):
        return obj._member_count
    member_count.short_description = "Members"


# ============================================
# CUSTOM USER ADMIN
# ============================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        "mobile",
        "full_name",
        "email",
        "family",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "family",
        "date_joined",
    )

    search_fields = (
        "mobile",
        "email",
        "fname",
        "lname",
        "family__name",
    )

    ordering = ("-date_joined",)

    autocomplete_fields = ("family",)

    readonly_fields = ("date_joined",)

    list_per_page = 25

    # ===============================
    # FIELDSETS (Edit View)
    # ===============================

    fieldsets = (
        ("Basic Info", {
            "fields": ("mobile", "password")
        }),
        ("Personal Info", {
            "fields": ("fname", "lname", "email", "family")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": ("date_joined",),
        }),
    )

    # ===============================
    # ADD USER FORM
    # ===============================

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "mobile",
                "email",
                "fname",
                "lname",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    # ===============================
    # CUSTOM DISPLAY METHODS
    # ===============================

    def full_name(self, obj):
        return f"{obj.fname} {obj.lname}"
    full_name.short_description = "Full Name"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("family")

    # ===============================
    # ADMIN ACTIONS
    # ===============================

    actions = ["make_staff", "remove_staff"]

    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"{updated} users promoted to staff.")
    make_staff.short_description = "Make selected users staff"

    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f"{updated} users removed from staff.")
    remove_staff.short_description = "Remove staff status"
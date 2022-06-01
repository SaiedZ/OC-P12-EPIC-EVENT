"""
Django admin customization for CRMUSer and Team models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from CRM.admin import crm_admin_site
from .models import Team


class UserAdminConfig(UserAdmin):
    """Define the admin pages for users."""

    search_fields = ("first_name", "email", "username", "team")
    list_filter = ("email", "username", "team")
    readonly_fields = ("is_staff", "is_active")
    ordering = (
        "team",
        "first_name",
    )
    list_display = (
        "first_name",
        "last_name",
        "email",
        "team",
        "username",
        "is_active",
        "is_staff",
        "phone",
        "mobile",
    )
    fieldsets = (
        (None, {"fields": ("email", "username")}),
        ("Departement", {"fields": ("team",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        (
            "Personal informations",
            {"fields": ("first_name", "last_name", "phone", "mobile")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "team",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "phone",
                    "mobile",
                ),
            },
        ),
    )


class TeamADmin(admin.ModelAdmin):

    fields = ["name"]
    list_display = ("name",)


admin.site.register(get_user_model())
admin.site.register(Team)

crm_admin_site.register(get_user_model(), UserAdminConfig)
crm_admin_site.register(Team, TeamADmin)

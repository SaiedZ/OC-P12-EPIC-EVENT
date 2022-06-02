"""
Django admin customization for CRMUSer and Team models.
"""

from django.contrib import admin
from django.contrib import auth
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

    # handle the permissions to perform CRUD on CRMUser and Temas data

    def get_user(self, request):
        """
        Return the request's user if it exists.
        :param request: The http request object.
        :return: user.
        """
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def is_management_permission(self, request):
        """
        Verrify if the request user belong to the management team.
        :param request: The http request object.
        :return: boolean.
        """
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Management']
        return False

    def has_add_permission(self, request):
        return self.is_management_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.is_management_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.is_management_permission(request)

    def has_view_permission(self, request, obj=None):
        return self.is_management_permission(request)

    def has_module_permission(self, request):
        return self.is_management_permission(request)


class TeamAdmin(admin.ModelAdmin):
    """Define the admin pages for Teams."""

    fields = ["name"]
    list_display = ("name",)

    def get_user(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def is_management_permission(self, request):
        """
        Verrify if the request user belong to the management team.
        :param request: The http request object.
        :return: boolean.
        """
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Management']
        return False

    def has_view_permission(self, request, obj=None):
        return self.is_management_permission(request)

    def has_module_permission(self, request):
        return self.is_management_permission(request)


admin.site.register(get_user_model())
admin.site.register(Team)

crm_admin_site.register(get_user_model(), UserAdminConfig)
crm_admin_site.register(Team, TeamAdmin)

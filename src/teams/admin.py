from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CRMUser, Team


class UserAdminConfig(UserAdmin):

    search_fields = ("first_name", "email", "username", "team")
    list_filter = ("email", "username", "team")
    ordering = ("team", "first_name",)
    list_display = ("team", "first_name", "last_name", "email",
                    "username", "is_active", "is_staff",
                    "phone", "mobile")
    fieldsets = (
        (None, {"fields": ("email", "username")}),
        ("Departement", {"fields": ("team",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Personal informations", {"fields": (
            "first_name", "last_name", "phone", "mobile")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "team",
                       "first_name", "last_name",
                       "password1", "password2",
                       "phone", "mobile")}
         ),
    )


admin.site.register(CRMUser, UserAdminConfig)
admin.site.register(Team)

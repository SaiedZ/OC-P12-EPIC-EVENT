from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CRMUser


class UserAdminConfig(UserAdmin):

    search_fields = ("first_name", "email", "username")
    list_filter = ("email", "username")
    ordering = ("first_name",)
    list_display = ("first_name", "last_name", "email",
                    "username", "is_active", "is_staff",
                    "phone", "mobile")
    fieldsets = (
        (None, {"fields": ("email", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Personal informations", {"fields": (
            "first_name", "last_name", "phone", "mobile")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username",
                       "first_name", "last_name",
                       "password1", "password2",
                       "phone", "mobile")}
         ),
    )


admin.site.register(CRMUser, UserAdminConfig)

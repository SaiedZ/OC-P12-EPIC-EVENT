"""
Django admin customization for Client model.
"""

from django import forms
from django.contrib import admin
from django.contrib import auth
from django.core.exceptions import ValidationError

from CRM.admin import crm_admin_site
from clients.models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

    def clean(self):

        cleaned_data = super().clean()

        phone = cleaned_data.get('phone', None)
        mobile = cleaned_data.get('mobile', None)
        if phone is not None or mobile is not None:
            return cleaned_data
        raise ValidationError("You must provide at least one phone number.")


class ClientAdmin(admin.ModelAdmin):

    form = ClientForm

    readonly_fields = ("date_created", "date_updated", "potential")

    search_fields = ("first_name", "last_name", "compagny_name", "email")
    list_filter = ("compagny_name", "potential")
    ordering = ("potential", "compagny_name")
    list_display = (
        "compagny_name",
        "first_name",
        "last_name",
        "email",
        "potential",
        "date_created",
        "date_updated",
    )

    fieldsets = (
        ("Client's information", {
            "fields": ("compagny_name", "first_name", "last_name", "potential")
        }),
        ("Contact information", {"fields": ("email", "phone", "mobile")}),
        (
            "Additionnal informations", {
                "fields": ("date_created", "date_updated"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_user(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def has_module_permission(self, request):
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale', 'Management']
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale', 'Management']
        return True

    def has_delete_permission(self, request, obj=None):
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale']
        return False

    def has_add_permission(self, request):
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale']
        return False

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale', 'Management']
        return True


crm_admin_site.register(Client, ClientAdmin)

admin.site.register(Client)

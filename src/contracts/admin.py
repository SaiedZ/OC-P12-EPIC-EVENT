"""
Django admin customization for Contract model.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import get_permission_codename  # noqa
from django.contrib import messages

from CRM.admin import crm_admin_site
from contracts.models import Contract


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = '__all__'

    def clean_sales_contact(self):
        sales_contact = self.cleaned_data['sales_contact']
        if sales_contact.team is not None \
           and sales_contact.team.name == "Sale":
            return sales_contact
        raise ValidationError("Sales contact must be part of the Sale team.")

    def save(self, commit=False):
        contract = super().save(commit=commit)
        client = contract.client
        if contract.status and client.potential:
            client.potential = False
            client.save()
        return contract


class ContractAdmin(admin.ModelAdmin):

    form = ContractForm

    readonly_fields = ("date_created", "date_updated")

    search_fields = ("sales_contact", "client", "status")
    list_filter = ("sales_contact", "status", "client")

    ordering = (
        "status",
        "date_created",
    )
    list_display = (
        "sales_contact",
        "client",
        "status",
        "amount",
        "payment_due",
        "date_created",
        "date_updated",
    )

    fieldsets = (
        ("EpicEvent Team", {
            "fields": ("sales_contact",),
            "description": "Only user from sale departement."
        }),
        ("Commercial", {"fields": ("client", "status")}),
        ("Economic informations", {"fields": ("amount", "payment_due")}),
        (
            "Additionnal informations", {
                "fields": ("date_created", "date_updated"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ['sign_contract']

    '''@admin.action(
        permissions=['sign_contract'],
        description='Sign a contract, allowed for sale contact',
    )'''

    def sign_contract(self, request, queryset):
        if hasattr(request.user, '_wrapped'):
            messages.add_message(
                request,
                messages.WARNING,
                ("Please note that only non signed contracts will be \
                    to be signed. And that's if your are the sales contact.\
                        Otherwise, th sign contract action will be ignored."))
            user = request.user._wrapped
        else:
            user = request.user
        for contract in queryset:
            if contract.sales_contact == user and not contract.status:
                contract.staus = True
                client = contract.client
                client.potential = False
                contract.save()
                client.save()

    sign_contract.short_description = "Sign contract"

    '''def has_sign_contract_permission(self, request):
        """Does the user have the sign contract permission?"""
        opts = self.opts
        # codename = get_permission_codename('sign_contract', opts)
        # return request.user.has_perm('%s.%s' % (opts.app_label, codename))
        print(request.POST.get('_selected_action', None))
        return True'''

    def get_user(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def has_add_permission(self, request):  # sourcery skip: class-extract-method # noqa
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale', 'Management']
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        user = self.get_user(request)
        if user.is_authenticated:
            return user == obj.sales_contact and not obj.status
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        user = self.get_user(request)
        if user.is_authenticated:
            return user == obj.sales_contact
        return False

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale', 'Management']
        return True

    def has_module_permission(self, request):
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Sale', 'Management']
        return False


crm_admin_site.register(Contract, ContractAdmin)

admin.site.register(Contract)

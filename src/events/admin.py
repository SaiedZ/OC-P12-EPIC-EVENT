"""
Django admin customization for Event and EventStatus models.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib import auth
from django.contrib import messages

from CRM.admin import crm_admin_site
from events.models import Event, EventStatus


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'

    def clean_support_contact(self):
        support_contact = self.cleaned_data['support_contact']
        if support_contact.team is not None \
           and support_contact.team.name == "Support":
            return support_contact
        raise ValidationError("Support contact must be part\
            of the Support team.")


class EventAdmin(admin.ModelAdmin):

    form = EventForm

    readonly_fields = ("date_created", "date_updated")

    search_fields = ("contract", "support_contact", "status")
    list_filter = ("support_contact", "status")

    ordering = (
        "status",
        "date_created",
    )
    list_display = (
        "support_contact",
        "contract",
        "status",
        "attendees",
        "event_date",
        "date_created",
        "date_updated",
    )

    fieldsets = (
        ("EpicEvent Team", {
            "fields": ("support_contact",),
            "description": "Only user from support departement."
        }),
        ("Commercial", {"fields": ("contract", "status")}),
        ("Organisation info", {"fields": ("attendees", "event_date", "notes")}),
        (
            "Additionnal informations", {
                "fields": ("date_created", "date_updated"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ['close_event']

    def close_event(self, request, queryset):
        status_finished = EventStatus.objects.filter(
                name="finished")[0]
        if hasattr(request.user, '_wrapped'):
            user = request.user._wrapped
        else:
            user = request.user
        queryset.filter(support_contact_id=user).update(status=status_finished)

    close_event.short_description = "Close finished events"

    def get_user(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def _is_management_sale_support_permission(self, request):
        user = self.get_user(request)
        if user.is_authenticated and user.team is not None:
            return user.team.name in ['Management', 'Sale', 'Support']
        return False

    def has_module_permission(self, request):
        return self._is_management_sale_support_permission(request)

    def has_view_permission(self, request, obj=None):
        return self._is_management_sale_support_permission(request)

    def has_add_permission(self, request, obj=None):
        return self._is_management_sale_support_permission(request)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        user = self.get_user(request)
        if user.is_authenticated:
            return user == obj.support_contact \
                and obj.status.name == "ongoing"
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        user = self.get_user(request)
        if user.is_authenticated:
            return user == obj.support_contact \
                and obj.status.name == "ongoing"
        return False


crm_admin_site.register(Event, EventAdmin)
crm_admin_site.register(EventStatus)

admin.site.register(Event)
admin.site.register(EventStatus)

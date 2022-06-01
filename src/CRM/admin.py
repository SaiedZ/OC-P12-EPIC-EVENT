"""
Custom Django admin site for the CRM database.
"""

from django.contrib import admin


class EpicEventCRMAdmin(admin.AdminSite):

    site_header = "The EpicEvent CRM Admin"
    index_title = "The EpicEvent CRM"
    site_title = "Admin UI"


crm_admin_site = EpicEventCRMAdmin(name="CRMAdmin")
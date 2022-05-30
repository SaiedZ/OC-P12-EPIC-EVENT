"""
Django admin customization for Contract model.
"""

from django.contrib import admin

from contracts.models import Contract

admin.site.register(Contract)

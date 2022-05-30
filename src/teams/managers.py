"""
Managers for the custom User and Team models.
"""

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Manager


class CustomAccountManager(BaseUserManager):
    """Manager for users."""

    def create_superuser(self, email, username, first_name,
                         last_name, password, **other_fields):
        """Create, save and return a new superuser."""

        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(email, username, first_name,
                                last_name, password, **other_fields)

    def create_user(self, email, username, first_name,
                    last_name, password, **other_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)
        user.save()

        return user


class UniqueNameManager(Manager):
    """
    Generic manager responsible of handling entities described with a unique
    name.
    """

    def get_or_create_from_names(self, names):
        """Gets or creates objects from comma-separated names."""
        objects = []
        names = [name.strip() for name in names.split(',') if name.strip()]
        for name in names:
            obj, _ = self.get_or_create(name=name)
            objects.append(obj)
        return objects

    def get_by_natural_key(self, name):
        """Allows to use name as a natural key during fixture serialization."""
        return self.get(name=name)

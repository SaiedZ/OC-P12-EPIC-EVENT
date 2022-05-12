from django.utils.translation import gettext_lazy as _
from django.db.models import Manager


class UniqueNameManager(Manager):
    """Generic manager responsible of handling entities described with a unique
    name."""

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

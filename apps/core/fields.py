from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _


class OrderField(models.PositiveIntegerField):
    description = _(
        "Auto-incrementing field that can be used to order objects. "
        "The value is automatically set to the next available integer based on "
        "the maximum value of the field for the given model, optionally filtered by "
        "other fields specified in the `for_fields` argument.",
    )

    def __init__(self, *args, for_fields=None, **kwargs):
        self.for_fields = for_fields
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value is not None:
            return value
        queryset = model_instance.__class__.objects.all()
        if self.for_fields is not None:
            query = {field: getattr(model_instance, field) for field in self.for_fields}
            queryset = queryset.filter(**query)
        max_value = queryset.aggregate(max_value=Max(self.attname))["max_value"]
        value = 0 if max_value is None else max_value + 1
        setattr(model_instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.for_fields is not None:
            kwargs["for_fields"] = self.for_fields
        return name, path, args, kwargs

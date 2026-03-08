from django.core.cache import cache
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import ATTRIBUTES_SCHEMA_CACHE_KEY
from .models import AttributesSchema


@receiver([post_save, post_delete], sender=AttributesSchema)
def clear_attributes_schema_cache(sender, **kwargs):
    cache.delete(ATTRIBUTES_SCHEMA_CACHE_KEY)

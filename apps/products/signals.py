from django.core.cache import cache
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AttributesSchema
from .utils import ATTR_SCHEMA_CACHE_KEY


@receiver([post_save, post_delete], sender=AttributesSchema)
def invalidate_attributes_schema_cache(sender, **kwargs):
    cache.delete(ATTR_SCHEMA_CACHE_KEY)

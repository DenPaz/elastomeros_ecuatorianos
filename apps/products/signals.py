from django.core.cache import cache
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import ATTRIBUTES_SCHEMA_CACHE_KEY
from .constants import CATEGORIES_CACHE_KEY
from .models import AttributesSchema
from .models import Category
from .models import Product


@receiver([post_save, post_delete], sender=AttributesSchema)
def invalidate_attributes_schema_cache(sender, **kwargs):
    cache.delete(ATTRIBUTES_SCHEMA_CACHE_KEY)


@receiver([post_save, post_delete], sender=Category)
@receiver([post_save, post_delete], sender=Product)
def invalidate_categories_cache(sender, **kwargs):
    cache.delete(CATEGORIES_CACHE_KEY)

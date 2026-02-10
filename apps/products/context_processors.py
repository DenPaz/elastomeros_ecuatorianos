from django.core.cache import cache

from .constants import PRODUCT_CATEGORIES_CACHE_KEY
from .models import Category


def product_categories(request):
    categories = cache.get(PRODUCT_CATEGORIES_CACHE_KEY)
    if categories is None:
        categories = list(
            Category.objects.active()
            .with_active_products_count()
            .only("id", "name", "slug")
            .order_by("name"),
        )
        cache.set(PRODUCT_CATEGORIES_CACHE_KEY, categories, 60 * 60)  # 1 hour
    return {"product_categories": categories}

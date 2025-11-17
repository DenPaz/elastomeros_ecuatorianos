from .models import Category


def product_categories(request):
    categories = Category.objects.filter(is_active=True).only("name", "slug")
    return {"product_categories": categories}

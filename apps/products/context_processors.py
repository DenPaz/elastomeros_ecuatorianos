from .models import Category


def product_categories(request):
    categories = Category.objects.active().only("name", "slug")
    return {"product_categories": categories}

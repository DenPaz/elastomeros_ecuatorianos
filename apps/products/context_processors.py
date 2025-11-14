from .models import Category


def product_categories(request):
    categories = Category.objects.filter(is_active=True)
    return {"category_list": categories}

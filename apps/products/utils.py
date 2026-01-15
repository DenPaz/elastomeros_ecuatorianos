def product_image_upload_to(instance, filename):
    return f"products/products/{instance.variant.product.slug}/{filename}"

def product_image_upload_to(instance, filename):
    return f"products/{instance.product.slug}/{filename}"

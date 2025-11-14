def product_variant_image_upload_to(instance, filename):
    return (
        f"products/{instance.product_variant.product.slug}/"
        f"{instance.product_variant.sku}/{filename}"
    )

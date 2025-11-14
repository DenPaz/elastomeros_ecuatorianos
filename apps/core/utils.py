from django.templatetags.static import static


def get_default_image_url():
    return static("images/default-image.png")

from django.templatetags.static import static


def get_user_upload_path(instance, filename):
    return f"users/{instance.user.id}/{filename}"


def get_default_profile_picture_url():
    return static("images/default-profile-picture.png")

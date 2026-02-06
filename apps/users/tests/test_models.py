import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.users.utils import get_default_avatar_url

from .factories import UserFactory
from .factories import UserProfileFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_str_method_returns_full_name_and_email(self):
        user = UserFactory(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )
        expected_str = "John Doe <john.doe@example.com>"
        assert str(user) == expected_str

    def test_email_field_is_unique(self):
        UserFactory(email="john.doe@example.com")
        with pytest.raises(IntegrityError):
            UserFactory(email="john.doe@example.com")

    def test_username_field_is_email(self):
        assert User.USERNAME_FIELD == "email"

    def test_required_fields(self):
        assert "first_name" in User.REQUIRED_FIELDS
        assert "last_name" in User.REQUIRED_FIELDS
        assert "email" not in User.REQUIRED_FIELDS


@pytest.mark.django_db
class TestUserProfileModel:
    def test_str_method_returns_user_full_name_and_email(self):
        user = UserFactory(
            first_name="Jane",
            last_name="Smith",
            email="janesmith@example.com",
        )
        profile = UserProfileFactory(user=user)
        expected_str = "Jane Smith <janesmith@example.com>"
        assert str(profile) == expected_str

    def test_get_avatar_url_method_returns_default_avatar_when_no_image(self):
        profile = UserProfileFactory()
        assert profile.get_avatar_url() == get_default_avatar_url()

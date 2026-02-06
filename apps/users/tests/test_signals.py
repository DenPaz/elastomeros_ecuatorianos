import pytest

from .factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_profile_creation_on_user_creation():
    user = UserFactory()
    assert hasattr(user, "profile")
    assert user.profile.user == user

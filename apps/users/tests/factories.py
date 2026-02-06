from factory import Faker
from factory import LazyAttributeSequence
from factory import SubFactory
from factory import Trait
from factory import post_generation
from factory.django import DjangoModelFactory
from factory.django import ImageField

from apps.users.models import User
from apps.users.models import UserProfile


class UserFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = LazyAttributeSequence(
        lambda o, n: (
            f"{o.first_name.lower()}.{o.last_name.lower()}.{n + 1}@example.com"
        ),
    )

    class Meta:
        model = User

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create and results and not cls._meta.skip_postgeneration_save:
            instance.save()


class UserProfileFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = UserProfile
        django_get_or_create = ["user"]

    class Params:
        with_avatar = Trait(avatar=ImageField(filename="avatar.jpg"))

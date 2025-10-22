from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    message = _("The file size must not exceed %(max_size)d %(unit)s.")
    code = "max_size"
    units = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}

    def __init__(self, max_size, unit="MB", message=None, code=None):
        unit = unit.upper()
        if unit not in self.units:
            raise ValueError(_("Unit '%(unit)s' is invalid.") % {"unit": unit})
        self.unit = unit
        self.max_size = max_size
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        file_size = value.size
        max_size_bytes = self.max_size * self.units[self.unit]
        if file_size > max_size_bytes:
            raise ValidationError(
                self.message,
                code=self.code,
                params={"max_size": self.max_size, "unit": self.unit},
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.max_size == other.max_size
            and self.unit == other.unit
            and self.message == other.message
            and self.code == other.code
        )

    def __hash__(self):
        return hash((self.max_size, self.unit, self.message, self.code))

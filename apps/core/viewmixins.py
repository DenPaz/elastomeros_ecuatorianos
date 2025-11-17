from collections.abc import Sequence

from django.core.exceptions import ImproperlyConfigured

TemplateSpec = str | Sequence[str]


class HtmxTemplateMixin:
    htmx_template_name: TemplateSpec | None = None

    def is_htmx(self) -> bool:
        return bool(getattr(self.request, "htmx", False))

    def get_template_names(self) -> list[str]:
        base_templates = super().get_template_names()
        if not self.is_htmx():
            return base_templates
        htmx_template = self.htmx_template_name
        if htmx_template is None:
            msg = (
                f"{self.__class__.__name__} is missing the "
                "'htmx_template_name' attribute, which is required "
                "for HTMX requests."
            )
            raise ImproperlyConfigured(msg)
        if isinstance(htmx_template, str):
            if htmx_template.startswith("#"):
                return [base_templates[0] + htmx_template]
            return [htmx_template]
        return list(htmx_template)

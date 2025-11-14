from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_class(
    context,
    *args,
    css_class="active",
    prefix_match=False,
    **kwargs,
):
    request = context.get("request")
    if not request:
        return ""
    resolver_match = getattr(request, "resolver_match", None)
    if not resolver_match:
        return ""
    current_view_name = resolver_match.view_name or ""
    if not current_view_name:
        return ""
    if prefix_match:
        matches = any(current_view_name.startswith(name) for name in args)
    else:
        matches = current_view_name in args
    if matches and kwargs:
        current_kwargs = resolver_match.kwargs or {}
        for key, value in kwargs.items():
            if str(current_kwargs.get(key, "")) != str(value):
                return ""
    return css_class if matches else ""

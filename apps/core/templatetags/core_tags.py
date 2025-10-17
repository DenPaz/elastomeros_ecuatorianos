from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_class(context, *view_names, css_class="active", prefix_match=False):
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
        matches = any(current_view_name.startswith(name) for name in view_names)
    else:
        matches = current_view_name in view_names
    return css_class if matches else ""

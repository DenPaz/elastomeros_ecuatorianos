from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_class(  # noqa: PLR0911
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
    current_view_name = resolver_match.view_name
    if not current_view_name:
        return ""
    if prefix_match:
        matches = any(current_view_name.startswith(name) for name in args)
    else:
        matches = current_view_name in args
    if not matches:
        return ""
    tag_params = {str(k): str(v) for k, v in kwargs.items()}
    request_params = {str(k): str(v) for k, v in (resolver_match.kwargs or {}).items()}
    query_params = {str(k): str(v) for k, v in request.GET.items() if k != "page"}
    request_params.update(query_params)
    if not tag_params:
        if not request_params:
            return css_class
        return ""
    for key, value in tag_params.items():
        if request_params.get(key) != value:
            return ""
    return css_class

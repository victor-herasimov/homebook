from django import template
from django.utils.http import urlencode


register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag(takes_context=True)
def elided_page_range(context, number, on_each_side=3, on_ends=2, **kwargs):
    paginator = context["page_obj"].paginator
    return list(
        paginator.get_elided_page_range(
            number, on_each_side=on_each_side, on_ends=on_ends
        )
    )


@register.simple_tag(takes_context=True)
def check_param(context, name, **kwargs):
    query_param = context["request"].GET.get(name, None)
    return True if query_param else False

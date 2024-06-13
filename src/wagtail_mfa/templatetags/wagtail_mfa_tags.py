from django.template import Library
from django.template.loader import render_to_string
from wagtail import VERSION

register = Library()


@register.simple_tag
def render_form_field(field):
    if VERSION >= (6, 0):
        return render_to_string(
            "wagtail_mfa/_compat/render_field_wagtail60.html",
            {"field": field},
        )

    return render_to_string(
        "wagtail_mfa/_compat/render_field_wagtail52.html",
        {"field": field},
    )

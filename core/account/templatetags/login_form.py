from django import template

from core.account.forms import UserLoginForm

register = template.Library()


@register.simple_tag
def user_login_form():
    form = UserLoginForm()
    return form

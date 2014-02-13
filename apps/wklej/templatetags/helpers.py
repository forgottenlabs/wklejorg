from django.conf import settings
from django.template import Library
from datetime import date

register = Library()


@register.simple_tag
def google_analytics_id():
    return settings.GOOGLE_ANALYTICS_ID

@register.simple_tag
def current_year():
    return date.today().year

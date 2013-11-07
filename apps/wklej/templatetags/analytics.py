
from django.conf import settings
from django.template import Library


register = Library()


@register.simple_tag
def google_analytics_id():
    return settings.GOOGLE_ANALYTICS_ID

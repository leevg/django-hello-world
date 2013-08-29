from django.core.urlresolvers import reverse
from django.template import Library

register = Library()


@register.simple_tag
def edit_tag(obj):
    url = "admin:%s_%s_change" % (
        obj._meta.app_label.lower(),
        obj._meta.module_name.lower(),
    )
    return reverse(url, args=(obj.pk, ))

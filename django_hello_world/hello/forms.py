from django.forms import ModelForm, DateInput
from django.utils.safestring import mark_safe

from models import UserInfo


class CalendarWidget(DateInput):
    class Media:
        css = {
            'all': ('css/jquery-ui-1.8.21.custom.css', )
        }
        js = (
            'js/jquery.min.js',
            'js/jquery-ui-1.8.21.custom.min.js',
        )

    def render(self, name, value, attrs=None):
        html = super(CalendarWidget, self).render(name, value, attrs)
        return mark_safe(
            html + '''<script type="text/javascript">$(function()
            {$('#%s').datepicker({dateFormat: 'yy-mm-dd',changeYear:
            true,changeMonth: true});});</script>''' %
            attrs['id'])


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ('first_name', 'last_name', 'date_of_birth', 'photo', 'email',
                  'jabber', 'skype', 'other_contacts', 'bio')
        widgets = {
            'date_of_birth': CalendarWidget(),
        }

    class Media:
        js = (
            'js/jquery.min.js',
            'js/contact_form.js'
        )

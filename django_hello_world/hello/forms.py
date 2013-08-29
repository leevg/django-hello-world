from django.forms import ModelForm, DateInput
from models import UserInfo


class CalendarWidget(DateInput):
    class Media:
        css = {
            'all': ('css/jquery-ui-1.8.21.custom.css', )
        }
        js = (
            'js/jquery.min.js',
            'js/jquery-ui-1.8.21.custom.min.js',
            'js/add_form.js',
        )


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ('first_name', 'last_name', 'date_of_birth', 'photo', 'email',
                  'jabber', 'skype', 'other_contacts', 'bio')

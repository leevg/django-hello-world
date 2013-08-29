from django.forms import ModelForm
from models import UserInfo


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ('first_name', 'last_name', 'date_of_birth', 'photo', 'email',
                  'jabber', 'skype', 'other_contacts', 'bio')

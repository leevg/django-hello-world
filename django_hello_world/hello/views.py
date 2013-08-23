from annoying.decorators import render_to
from django.contrib.auth.models import User
from models import UserInfo

@render_to('hello/home.html')
def home(request):
    userinfo = UserInfo.objects.get(pk=1)
    return {'userinfo': userinfo}

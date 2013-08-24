from annoying.decorators import render_to
from django.contrib.auth.models import User
from models import UserInfo, RequestInfo

@render_to('hello/home.html')
def home(request):
    userinfo = UserInfo.objects.get(pk=1)
    return {'userinfo': userinfo}

@render_to('hello/requests.html')
def requests(request):
    requestinfo = RequestInfo.objects.all()[:10]
    return {'requests':requestinfo}
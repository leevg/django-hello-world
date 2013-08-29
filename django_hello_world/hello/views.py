from annoying.decorators import render_to

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from forms import UserInfoForm

from models import UserInfo, RequestInfo


@render_to('hello/home.html')
def home(request):
    userinfo = UserInfo.objects.get(pk=1)
    return {'userinfo': userinfo}


@render_to('hello/requests.html')
def requests(request):
    requestinfo = RequestInfo.objects.all()[:10]
    return {'requests': requestinfo}


@render_to('hello/home.html')
def user_info_edit(request):
    userinfo = UserInfo.objects.get(pk=1)
    return {'userinfo': userinfo}


@login_required
def user_info_edit(request):
    userinfo = get_object_or_404(UserInfo)
    if request.method == 'POST':
        form = UserInfoForm(request.POST, request.FILES, instance=userinfo)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return HttpResponse("success")
            else:
                return redirect(reverse('home'))
    else:
        form = UserInfoForm(instance=userinfo)
    return render(request, 'hello/edit.html', {'form': form})

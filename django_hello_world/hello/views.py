from annoying.decorators import render_to

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from forms import UserInfoForm, RequestInfoFormSet

from models import UserInfo, RequestInfo


@render_to('hello/home.html')
def home(request):
    userinfo = UserInfo.objects.get(pk=1)
    return {'userinfo': userinfo}


@render_to('hello/requests.html')
def requests(request):
    requestinfos = RequestInfo.objects.all()[:10]
    formset = RequestInfoFormSet(queryset=requestinfos)
    objects = zip(requestinfos, formset)
    return {'objects': objects, 'formset': formset}


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


@login_required
def priority_update(request):
    if request.method == 'POST':
        formset = RequestInfoFormSet(request.POST)

        if formset.is_valid():
            formset.save()

    return redirect('requests')

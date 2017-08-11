from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView

User = get_user_model()

from .forms import CreateUserForm, UserLoginForm

@login_required(login_url='/login')
def register_view(request, *args, **kwargs):
    permissions = False
    if request.user.profile.user_type == 'A':
        permissions = True
    template_name = 'registration/register.html'
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    return render(request, template_name, {'form': form, 'permissions': permissions})

def login_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/courses')
    template_name = 'registration/login.html'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username_ = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=username_)
        print(user_obj)
        login(request, user_obj)
        return HttpResponseRedirect(request.POST.get('next'))
    return render(request, template_name, {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

class StudentsView(ListView):
    model =ListView
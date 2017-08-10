from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required

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
        return HttpResponseRedirect('/admin')
    return render(request, template_name, {'form': form, 'permissions': permissions})

def login_view(request, *args, **kwargs):
    template_name = 'registration/login.html'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username_ = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=username_)
        print(user_obj)
        login(request, user_obj)
        return HttpResponseRedirect("/register")
    return render(request, template_name, {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")
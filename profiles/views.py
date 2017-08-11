from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from .models import *

User = get_user_model()

from .forms import CreateUserForm, UserLoginForm

@login_required(login_url='/profiles/login')
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
        return HttpResponseRedirect('/courses')
    return render(request, template_name, {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/profiles/login')

class StudentsView(LoginRequiredMixin,ListView):
    model = Profile

    login_url = '/profiles/login'

    def get_queryset(self):
        return Profile.objects.filter(Q(user_type__iexact='S') & Q(user__is_active=True))

    def get_context_data(self, **kwargs):
        context = super(StudentsView, self).get_context_data(**kwargs)
        context['type'] = 'S'
        return context

class TeachersView(LoginRequiredMixin, ListView):
    model = Profile

    login_url = '/profiles/login'

    def get_queryset(self):
        return Profile.objects.filter(Q(user_type__iexact='T') & Q(user__is_active=True))

    def get_context_data(self, **kwargs):
        context = super(TeachersView, self).get_context_data(**kwargs)
        context['type'] = 'T'
        return context

class GroupsView(LoginRequiredMixin, ListView):
    model = ProfileGroup

    login_url = '/profiles/login'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['full_name',
              'birth_date']

    login_url = '/profiles/login'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        return context
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView

from .models import *

User = get_user_model()

from .forms import CreateUserForm, UserLoginForm, UpdateStudentForm, UpdateTeacherForm

@login_required(login_url='/profiles/login')
def register_view(request, *args, **kwargs):
    permissions = False
    if request.user.profile.user_type == 'A':
        permissions = True
    template_name = 'registration/register.html'
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        if form.cleaned_data['user_type'] == 'T':
            return HttpResponseRedirect('/profiles/teachers')
        elif form.cleaned_data['user_type'] == 'S':
            return HttpResponseRedirect('/profiles/students')
        else:
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

class UpdateStudentView(UpdateView):
    model = Profile
    form_class = UpdateStudentForm
    success_url = '/profiles/students'

    user_full_name = ''

    def get_object(self, queryset=None):
        profile = Profile.objects.filter(pk=self.kwargs['pk'])[0]
        self.user_full_name = profile.full_name
        return profile

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        context['user_full_name'] = self.user_full_name
        return context

class UpdateTeacherView(UpdateView):
    model = Profile
    form_class = UpdateTeacherForm
    success_url = '/profiles/teachers'

    user_full_name = ''

    def get_object(self, queryset=None):
        profile = Profile.objects.filter(pk=self.kwargs['pk'])[0]
        self.user_full_name = profile.full_name
        return profile

    def get_context_data(self, **kwargs):
        context = super(UpdateTeacherView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        context['user_full_name'] = self.user_full_name
        return context

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = ProfileGroup

    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        object = kwargs.get('object')
        students = Profile.objects.filter(group=object.pk)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        context['students'] = students
        context['group_name'] = object.name
        context['group_id'] = object.pk
        return context

class GroupDeleteView(DeleteView):
    model = ProfileGroup
    success_url = '/profiles/groups'

class GroupCreateView(CreateView):
    model = ProfileGroup
    success_url = '/profiles/groups'
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        return context
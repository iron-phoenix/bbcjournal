from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

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
        if not user_obj.profile.is_password_changed:
            return redirect('profiles:change_password')
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

class UpdateStudentView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateStudentForm
    success_url = '/profiles/students'

    login_url = '/profiles/login'

    user_full_name = ''
    username = ''
    user_type = ''
    user_id = ''

    def get_object(self, queryset=None):
        profile = Profile.objects.filter(pk=self.kwargs['pk'])[0]
        self.user_full_name = profile.full_name
        self.username = profile.user.username
        self.user_type = profile.user_type
        self.user_id = profile.pk
        return profile

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        context['user_full_name'] = self.user_full_name
        context['username'] = self.username
        context['user_type'] = self.user_type
        context['user_id'] = self.user_id
        return context

class UpdateTeacherView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateTeacherForm
    success_url = '/profiles/teachers'

    login_url = '/profiles/login'

    user_full_name = ''
    username = ''
    user_type = ''
    user_id = ''

    def get_object(self, queryset=None):
        profile = Profile.objects.filter(pk=self.kwargs['pk'])[0]
        self.user_full_name = profile.full_name
        self.username = profile.user.username
        self.user_type = profile.user_type
        self.user_id = profile.pk
        return profile

    def get_context_data(self, **kwargs):
        context = super(UpdateTeacherView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        context['user_full_name'] = self.user_full_name
        context['username'] = self.username
        context['user_type'] = self.user_type
        context['user_id'] = self.user_id
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

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ProfileGroup
    success_url = '/profiles/groups'

    login_url = '/profiles/login'

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = ProfileGroup
    success_url = '/profiles/groups'
    fields = ['name']

    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        return context

@login_required(login_url='/profiles/login')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.profile.is_password_changed = True
            user.profile.save()
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('courses:courses')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {
        'form': form,
        'user_name': request.user.username,
        'is_password_changed': request.user.profile.is_password_changed
    })
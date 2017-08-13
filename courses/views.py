from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Course, Lesson

# Create your views here.

class CoursesView(LoginRequiredMixin, ListView):
    model = Course

    login_url = '/profiles/login'

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course

    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        object = kwargs.get('object')
        lessons = Lesson.objects.filter(course=object.pk)
        context['lessons'] = lessons
        return context

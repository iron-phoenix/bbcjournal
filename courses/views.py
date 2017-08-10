from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Course, Lesson

# Create your views here.

class CoursesView(ListView):
    model = Course

class CourseDetailView(DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        object = kwargs.get('object')
        lessons = Lesson.objects.filter(course=object.pk)
        context['lessons'] = lessons
        return context

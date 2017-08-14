from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Course, Lesson, StudentLesson
from .forms import LessonCreateForm

from profiles.models import Profile

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

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonCreateForm
    success_url = '/courses'

    def get_context_data(self, **kwargs):
        context = super(LessonCreateView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'T':
            permissions = True
        context['permissions'] = permissions
        return context

    def form_valid(self, form):
        form.instance.teacher = Profile.objects.filter(user=self.request.user)[0]
        form.save()

        lesson = super(LessonCreateForm, form).save(commit=False)

        group = form.cleaned_data.get('group')
        students = Profile.objects.filter(group=group)

        for student in students:
            student_lesson = StudentLesson(student = student, lesson = lesson)
            student_lesson.save()

        return super(LessonCreateView, self).form_valid(form)

class LessonDetailView(DetailView):
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        lesson = kwargs['object']
        student_lessons = StudentLesson.objects.filter(lesson=lesson)
        context['student_lessons'] = student_lessons
        return context


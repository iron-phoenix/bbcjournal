from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.db.models import Q

from .models import Course, Lesson, StudentLesson
from .forms import LessonCreateForm, StudentLessonEditForm

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

    def get_success_url(self):
        return '/courses/edit_lesson/' + str(self.object.pk)

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

class LessonEditView(UpdateView):
    model = Lesson
    fields = ['homework']
    template_name = 'courses/student_lesson_edit.html'

def get_students_pk(post):
    pks = {}
    for key in post:
        f = key.find('-')
        if f >= 0:
            n = key[f + 1:]
            if n not in pks:
                pks[n] = {}
            pks[n][key[:f]] = post[key]
    return pks

def lesson_edit_view(request, *args, **kwargs):
    permissions = False
    if request.user.profile.user_type == 'T':
        permissions = True
    template_name = 'courses/student_lesson_edit.html'
    if request.POST:
        pks = get_students_pk(request.POST)
        for pk in pks:
            student_lesson = StudentLesson.objects.filter(Q(student = pk) & Q(lesson = kwargs.get('pk')))[0]
            if 'precense' in pks[pk]:
                student_lesson.precense = True
            else:
                student_lesson.precense = False
            if student_lesson.precense:
                student_lesson.mark = pks[pk]['mark']
            else:
                student_lesson.reason_for_abcense = pks[pk]['reason_for_abcense']
            student_lesson.save()
        return HttpResponseRedirect('/')
    else:
        student_lessons = StudentLesson.objects.filter(lesson = kwargs.get('pk'))
        return render(request, template_name, {'student_lessons': student_lessons, 'permissions': permissions})


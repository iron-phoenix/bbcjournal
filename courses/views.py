from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Course, Lesson, StudentLesson
from .forms import LessonCreateForm, StudentLessonEditForm

from profiles.models import Profile, ProfileGroup

# Create your views here.

class CoursesView(LoginRequiredMixin, ListView):
    model = Course

    login_url = '/profiles/login'

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = '__all__'
    success_url = '/courses'

    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        permissions = False
        if self.request.user.profile.user_type == 'A':
            permissions = True
        context['permissions'] = permissions
        return context

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course

    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        object = kwargs.get('object')
        lessons = Lesson.objects.filter(course=object.pk)
        context['lessons'] = lessons
        return context

class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonCreateForm

    login_url = '/profiles/login'

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

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson

    login_url = '/profiles/login'

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        lesson = kwargs['object']
        student_lessons = StudentLesson.objects.filter(lesson=lesson)
        context['student_lessons'] = student_lessons
        return context

class LessonEditView(LoginRequiredMixin, UpdateView):
    model = Lesson
    fields = ['homework']
    template_name = 'courses/student_lesson_edit.html'

    login_url = '/profiles/login'

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

@login_required(login_url='/profiles/login')
def lesson_edit_view(request, *args, **kwargs):
    permissions = False
    if request.user.profile.user_type == 'T':
        permissions = True
    template_name = 'courses/student_lesson_edit.html'
    if request.POST:
        pks = get_students_pk(request.POST)
        for pk in pks:
            student_lesson = StudentLesson.objects.filter(Q(student = pk) & Q(lesson = kwargs.get('pk')))[0]
            student_lesson.lesson.homework = request.POST['homework']
            student_lesson.lesson.save()
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

@login_required(login_url='/profiles/login')
def teacher_lessons_view(request, *args, **kwargs):
    template_name = 'courses/teacher_lessons.html'
    profile = Profile.objects.filter(pk=kwargs['pk'])[0]
    user_full_name = profile.full_name
    lessons_query = Lesson.objects.filter(teacher=kwargs['pk']).order_by('-id')[:10]
    lessons = []
    n = 0
    for lesson in lessons_query:
        lessons.append({})
        lessons[n]['name'] = lesson.name
        lessons[n]['date'] = lesson.date
        lessons[n]['type'] = lesson.get_type_display()
        lessons[n]['course'] = lesson.course.name
        students = StudentLesson.objects.filter(lesson=lesson)
        lessons[n]['students'] = len(students)
        n += 1

    return render(request, template_name, {'lessons': lessons, 'user_full_name': user_full_name})

@login_required(login_url='/profiles/login')
def student_lessons_view(request, *args, **kwargs):
    template_name = 'courses/student_lessons.html'
    profile = Profile.objects.filter(pk=kwargs['pk'])[0]
    user_full_name = profile.full_name
    lessons = StudentLesson.objects.filter(student=kwargs['pk']).order_by('-id')[:10]
    return render(request, template_name, {'lessons': lessons, 'user_full_name': user_full_name})

@login_required(login_url='/profiles/login')
def group_journal_view(request, *args, **kwargs):
    template_name = 'courses/group_journal.html'
    group = ProfileGroup.objects.filter(pk=kwargs['pk'])[0]
    students = Profile.objects.filter(group=group)
    student_lessons = []
    for student in students:
        student_lessons_query = StudentLesson.objects.filter(student=student)[:10]
        student_lessons.append(student_lessons_query)
    return render(request, template_name, {'student_lessons': student_lessons})


from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^add_lesson', LessonCreateView.as_view(), name = 'add_lesson'),
    url(r'^lesson/(?P<pk>\d+)', LessonDetailView.as_view(), name = 'lesson_detail'),
    url(r'^edit_lesson/(?P<pk>\d+)', lesson_edit_view, name = 'lesson_edit'),
    url(r'^teacher_lesson/(?P<pk>\d+)', teacher_lessons_view, name = 'teacher_lessons'),
    url(r'^student_lesson/(?P<pk>\d+)', student_lessons_view, name = 'student_lessons'),
    url(r'^group_journal/(?P<pk>\d+)', group_journal_view, name = 'group_journal'),

    url(r'^create', CourseCreateView.as_view(), name='course_create'),
    url(r'(?P<pk>\d+)', CourseDetailView.as_view(), name='course_detail'),
    url(r'^$', CoursesView.as_view(), name='courses')
]
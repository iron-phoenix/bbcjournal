from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^add_lesson', LessonCreateView.as_view(), name = 'add_lesson'),
    url(r'^lesson/(?P<pk>\d+)', LessonDetailView.as_view(), name = 'lesson_detail'),

    url(r'(?P<pk>\d+)', CourseDetailView.as_view(), name='course_detail'),
    url(r'^$', CoursesView.as_view(), name='courses')
]
from django.conf.urls import url
from .views import CoursesView, CourseDetailView

urlpatterns = [
    url(r'(?P<pk>\d+)', CourseDetailView.as_view(), name='coursedetail'),
    url(r'^$', CoursesView.as_view(), name='courses')
]
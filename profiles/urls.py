from django.conf.urls import url

from .views import *

urlpatterns =[
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^password/', change_password_view, name='change_password'),

    url(r'^students/(?P<pk>\d+)', UpdateStudentView.as_view(), name='students_detail'),
    url(r'^teachers/(?P<pk>\d+)', UpdateTeacherView.as_view(), name='teachers_detail'),

    url(r'^groups/add', GroupCreateView.as_view(), name='groups_add'),
    url(r'^groups/delete/(?P<pk>\d+)', GroupDeleteView.as_view(), name='groups_delete'),
    url(r'^groups/(?P<pk>\d+)', GroupDetailView.as_view(), name='groups_detail'),

    url(r'^students', StudentsView.as_view(), name='students'),
    url(r'^teachers', TeachersView.as_view(), name='teachers'),
    url(r'^groups', GroupsView.as_view(), name='groups'),
]
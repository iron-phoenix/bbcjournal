from django.conf.urls import url

from .views import *

urlpatterns =[
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),

    url(r'^users/students', StudentsView.as_view(), name='students'),
    url(r'^users/teachers', TeachersView.as_view(), name='teachers'),
    url(r'^users/groups', GroupsView.as_view(), name='groups'),

    url(r'^users/(?P<pk>\d+)', UserUpdateView.as_view(), name='user_update')
]
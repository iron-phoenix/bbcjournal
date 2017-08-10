from django.conf.urls import url, include
from django.contrib import admin

from profiles.views import register_view, login_view, logout_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
]

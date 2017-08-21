from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

from profiles.views import register_view, login_view, logout_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^profiles/', include('profiles.urls', namespace='profiles')),

    url(r'^courses/', include('courses.urls', namespace='courses')),

    url(r'^$', RedirectView.as_view(url='courses/'))
]

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import CreateUserForm
from django.views.generic.edit import FormView

def create_user_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'registration/create_user.html', {})

# class CreateUserView(FormView):
#     template_name = 'registration/create_user.html'
#     form_class = CreateUserForm
#     success_url = 'registration/create_user.html'
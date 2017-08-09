from django.contrib.messages.views import SuccessMessageMixin

from .forms import CreateUserForm
from django.views.generic.edit import CreateView

class CreateUserView(SuccessMessageMixin, CreateView):
    template_name = 'registration/create_user.html'
    form_class = CreateUserForm
    success_url = '/'
    success_message = "Your account was created successfully"
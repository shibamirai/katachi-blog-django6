from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm
from .models import CustomUser

class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'customauth/login.html'


class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'customauth/register.html'
    success_url = reverse_lazy('customauth:login')
    
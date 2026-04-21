from django.contrib.auth.views import LoginView as BaseLoginView

from .forms import LoginForm

class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'customauth/login.html'

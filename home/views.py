from datetime import datetime
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import redirect

# Rest of your views.py file...


class SignupView(CreateView):
    """
    Handles user signup functionality.
    Redirects authenticated users to the notes list page.
    """
    form_class = UserCreationForm
    template_name = 'home/register.html'
    success_url = '/smart/notes'

    def get(self, request, *args, **kwargs):
        # Redirect authenticated users to notes list
        if self.request.user.is_authenticated:
            return redirect('notes.list')
        return super().get(request, *args, **kwargs)


class LogoutInterfaceView(LogoutView):
    """
    Handles user logout functionality.
    """
    template_name = 'home/logout.html'


class LoginInterfaceView(LoginView):
    """
    Handles user login functionality.
    """
    template_name = 'home/login.html'



class HomeView(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'today': datetime.today()}



class AuthorizedView(LoginRequiredMixin, TemplateView):
    """
    Displays an authorized-only view.
    Redirects unauthenticated users to the login page.
    """
    template_name = 'home/authorized.html'
    login_url = '/login'  # Use /login instead of /admin for better UX

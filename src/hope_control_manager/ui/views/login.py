from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView


class LoginView(BaseLoginView):
    next_page = "/"
    redirect_authenticated_user = True
    redirect_field_name = None


class LogoutView(BaseLogoutView):
    def get_success_url(self) -> str:
        return "/"

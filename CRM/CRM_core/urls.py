from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy

from .forms import ResetPasswordForm
from .views import IndexView, LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('api/', include('CRM_core.api.urls')),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('login'),
             template_name="CRM_core/password_reset_confirm.html",
             form_class=ResetPasswordForm), name='password_reset_confirm'),
]

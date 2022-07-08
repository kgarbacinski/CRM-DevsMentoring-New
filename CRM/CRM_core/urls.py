from django.contrib.auth.views import LogoutView
<<<<<<< HEAD
from django.urls import path, include, reverse_lazy

from .forms import ResetPasswordForm
from .views import IndexView, LoginView
from django.contrib.auth import views as auth_views
=======
from django.urls import include, path, re_path

from .views import IndexView, LoginView

# from django.views.generic.base import RedirectView
>>>>>>> feat/Add-pre-hooks


urlpatterns = [
<<<<<<< HEAD
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('api/', include('CRM_core.api.urls')),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('login'),
             template_name="CRM_core/password_reset_confirm.html",
             form_class=ResetPasswordForm), name='password_reset_confirm'),
=======
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("index/", IndexView.as_view(), name="index"),
    path("api/", include("CRM_core.api.urls")),
>>>>>>> feat/Add-pre-hooks
]

from django.contrib.auth.views import LogoutView
from django.urls import include, path, re_path

from .views import IndexView, LoginView

# from django.views.generic.base import RedirectView

# favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("index/", IndexView.as_view(), name="index"),
    path("api/", include("CRM_core.api.urls")),
]

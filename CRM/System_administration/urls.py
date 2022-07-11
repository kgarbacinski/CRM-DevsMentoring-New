from django.urls import include, path

from System_administration.views import SummaryView

urlpatterns = [
    path("", SummaryView.as_view(), name="summary"),
    path("api/", include("System_administration.api.urls")),
]

from django.urls import include, path
from Files_organizer.views import ProgramingPathView, SubjectView, TopicView

urlpatterns = [
    path("", ProgramingPathView.as_view(), name="programming_path"),
    path("<slug:path>/", SubjectView.as_view(), name="subject"),
    path("<slug:path>/<slug:subject>/", TopicView.as_view(), name="topic"),
    path("api/", include("Files_organizer.api.urls")),
]

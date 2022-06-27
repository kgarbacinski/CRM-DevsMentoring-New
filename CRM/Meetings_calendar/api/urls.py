from django.urls import path

from .views import (
    AddMeeting,
    EditDeleteMeeting,
    EditDeleteNote,
    ListMeetings,
    ListNotes,
    ListStudents,
    MeetingDetail,
)

urlpatterns = [
    path("notes/", ListNotes.as_view(), name="notes"),
    path("edit-note/<int:pk>/", EditDeleteNote.as_view(), name="editNote"),
    path("meetings/", ListMeetings.as_view(), name="meetings"),
    path("meeting-detail/", MeetingDetail.as_view(), name="meeting"),
    path("add-meeting/", AddMeeting.as_view(), name="add_meeting"),
    path("edit-meeting/<int:pk>/", EditDeleteMeeting.as_view(), name="edit_meeting"),
    path("students/", ListStudents.as_view(), name="students"),
]

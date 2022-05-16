from django.urls import path

from CRM_core.api.views import ListMeetingsByDates, ChangeAvatar, GetNoteText

urlpatterns = [
    path('meetings-range/', ListMeetingsByDates.as_view(), name='meetings-range'),
    path('change-avatar/<int:pk>/', ChangeAvatar.as_view(), name='change_avatar'),
    path('get-note/', GetNoteText.as_view())
]

from django.urls import path

from System_administration.api.views import ListAllMeetings, GetPathsList, GetStudentsList, GetMeetingDates, \
    GetMentorsList

urlpatterns = [
    path('all-meetings/', ListAllMeetings.as_view(), name='all_meetings'),
    path('all-mentors/', GetMentorsList.as_view(), name='all_mentors'),
    path('all-students/', GetStudentsList.as_view(), name='all_students'),
    path('all-paths/', GetPathsList.as_view(), name='all_paths'),
    path('meeting-dates/', GetMeetingDates.as_view(), name='meetings_dates'),
]
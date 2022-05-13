from django.urls import path, include
from .views import CalendarView


urlpatterns = [
    path('', CalendarView.as_view(), name='calendar'),
    path('api/', include('Meetings_calendar.api.urls')),
]
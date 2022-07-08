from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class CalendarView(LoginRequiredMixin, View):
    template_name = "Meetings_calendar/calendar.html"
    login_url = "login"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

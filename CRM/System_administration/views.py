from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

# Create your views here.
from Meetings_calendar.models import Meeting


class SummaryView(LoginRequiredMixin, View):
    template_name = "System_administration/summary-view.html"
    model = Meeting

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name="Moderator").exists():
            return render(request, self.template_name, context={"is_moderator": True})
        elif user.groups.filter(name="Mentor").exists():
            return render(request, self.template_name, context={"is_moderator": False})
        return redirect("index")

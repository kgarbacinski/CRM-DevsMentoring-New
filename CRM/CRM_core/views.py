from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import LoginForm, ResetRequestForm
from .models import Mentor, Student


class LoginView(PasswordResetView):
    template_name = "CRM_core/login.html"

    def authenticate_user(self, user):
        user = user.save(commit=False)
        user = User.objects.get(email=user.email)
        login(request=self.request, user=user)
        next_page = self.request.GET.get("next", None)
        if next_page:
            return redirect(next_page)
        return redirect("index")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")

        return render(
            request,
            self.template_name,
            {"login_form": LoginForm(), "reset_form": ResetRequestForm()},
        )

    def post(self, request, *args, **kwargs):
        if "sing_in" in request.POST:
            user = LoginForm(request.POST)
            if user.is_valid():
                return self.authenticate_user(user)
        elif "send_reset" in request.POST:
            reset_form = ResetRequestForm(request.POST)

            if reset_form.is_valid():
                opts = {
                    "use_https": self.request.is_secure(),
                    "token_generator": self.token_generator,
                    "from_email": self.from_email,
                    "email_template_name": self.email_template_name,
                    "subject_template_name": self.subject_template_name,
                    "request": self.request,
                    "html_email_template_name": self.html_email_template_name,
                    "extra_email_context": self.extra_email_context,
                }
                reset_form.save(**opts)

        return render(
            request,
            self.template_name,
            {
                "login_form": LoginForm(request.POST),
                "reset_form": ResetRequestForm(request.POST),
            },
        )


class IndexView(LoginRequiredMixin, ListView):
    template_name = "CRM_core/index.html"
    context_object_name = "students"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Student").exists():
            return Mentor.objects.filter(student__user__username=user)
        return Student.objects.filter(mentor__user__username=user)

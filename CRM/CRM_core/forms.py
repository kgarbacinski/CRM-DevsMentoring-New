from CRM_core.exceptions import WrongPassword
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"id": "login-email"}), label="E-mail"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "login-password"}), label="Password"
    )
    error_messages = {"email": " Wrong email or password"}

    def validate_password(self, user):
        password = self.cleaned_data.get("password")
        validator = user.check_password(password)
        if not validator:
            raise WrongPassword

    def clean(self):
        super().clean()

        email = self.cleaned_data.get("email")
        try:

            user = User.objects.get(email=email)
            self.validate_password(user)

        except (User.DoesNotExist, WrongPassword):

            self._errors["email"] = self.error_messages["email"]

        return self.cleaned_data

    class Meta:
        model = User
        fields = ["email", "password"]


class ResetRequestForm(PasswordResetForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"id": "reset-email"}), label="E-mail"
    )
    error_messages = {"email": "Email doesn't exists"}

    def clean(self):
        super().clean()
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)

        except User.DoesNotExist:
            self._errors["email"] = self.error_messages["email"]
        return self.cleaned_data


class ResetPasswordForm(SetPasswordForm):
    error_css_class = "text-error"

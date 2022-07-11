from Payments_system.models import PaymentInfo
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class PaymentForm(forms.ModelForm):
    student = forms.CharField(
        required=None, widget=forms.TextInput(attrs={"id": "student"}), label="student"
    )
    firstName = forms.CharField(
        widget=forms.TextInput(attrs={"id": "name"}), label="name"
    )
    lastName = forms.CharField(
        widget=forms.TextInput(attrs={"id": "last-name"}), label="last-name"
    )
    companyName = forms.CharField(
        required=None, widget=forms.TextInput(attrs={"id": "company"}), label="company"
    )
    nip = forms.CharField(
        required=None,
        max_length=10,
        widget=forms.TextInput(attrs={"id": "company-nip"}),
        label="company-nip",
    )
    street = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": "adress", "placeholder": "Street and house / flat number"}
        ),
        label="street",
    )
    postCode = forms.CharField(
        widget=forms.TextInput(attrs={"id": "post-code"}), label="post-code"
    )
    town = forms.CharField(widget=forms.TextInput(attrs={"id": "city"}), label="city")
    country = forms.CharField(
        widget=forms.TextInput(attrs={"id": "country"}), label="country"
    )
    phone = PhoneNumberField(region="PL", widget=forms.TextInput(attrs={"id": "phone"}))
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"id": "email", "name": "email"})
    )
    comment = forms.CharField(
        required=None, widget=forms.Textarea(attrs={"id": "information", "rows": "3"})
    )

    class Meta:
        model = PaymentInfo
        fields = "__all__"

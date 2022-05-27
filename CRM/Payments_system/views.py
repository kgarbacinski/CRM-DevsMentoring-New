from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect


# Create your views here.
from django.views.generic import View

from CRM_core.models import Student
from Payments_system.forms import PaymentForm
from Payments_system.models import PaymentInfo


class PaymentView(LoginRequiredMixin, View):
    template_name = 'Payments_system/payment.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Mentor').exists():
            return render(request, self.template_name, {'form': PaymentForm()})
        try:
            payment_data = PaymentInfo.objects.get(student=Student.objects.get(user=request.user.id))
            form = PaymentForm(instance=payment_data)
            return render(request, self.template_name, {'form': form})
        except PaymentInfo.DoesNotExist:
            return render(request, self.template_name,
                          {'form': PaymentForm(initial=
                                               {'firstName': request.user.first_name,
                                                'lastName': request.user.last_name,
                                                'email': request.user.email})})

    # def post(self, request, *args, **kwargs):
    #     form = PaymentForm(request.POST)
    #     form.instance.user = request.user.id
    #     user = request.user
    #     if form.is_valid():
    #         if self.request.user.groups.filter(name='Student').exists():
    #             PaymentInfo.objects.update_or_create(
    #                 student=Student.objects.get(user=request.user.id),
    #                 defaults={'firstName': form.cleaned_data.get('firstName'),
    #                           'lastName': form.cleaned_data.get('lastName'),
    #                           'companyName': form.cleaned_data.get('companyName', ''),
    #                           'nip': form.cleaned_data.get('nip', ''),
    #                           'street': form.cleaned_data.get('street'),
    #                           'postCode': form.cleaned_data.get('postCode'),
    #                           'town': form.cleaned_data.get('town'),
    #                           'country': form.cleaned_data.get('country'),
    #                           'phone': form.cleaned_data.get('phone'),
    #                           'email': form.cleaned_data.get('email'),
    #                           'comment': form.cleaned_data.get('comment', '')}
    #             )
    #         Payment = get_payment_model()
    #         payment = Payment.objects.create(
    #             variant="przelewy24",  # this is the variant from PAYMENT_VARIANTS
    #             description=user.student.path.name,
    #             total=Decimal(user.student.path.price),
    #             # total=Decimal(0.1),
    #             # tax=Decimal(20),
    #             currency="PLN",
    #             # delivery=Decimal(10),
    #             billing_first_name=form.cleaned_data.get('firstName'),
    #             billing_last_name=form.cleaned_data.get('lastName'),
    #             billing_address_1=form.cleaned_data.get('street'),
    #             # billing_address_2="",
    #             billing_city=form.cleaned_data.get('town'),
    #             billing_postcode=form.cleaned_data.get('postCode'),
    #             billing_country_code="PL",
    #             billing_country_area=form.cleaned_data.get('country'),
    #             customer_ip_address="127.0.0.1",
    #             billing_email=form.cleaned_data.get('email'),
    #             # success_url='Account_management/index.html'
    #         )
    #         return redirect(f"/payment_details/{payment.pk}")
    #     return render(request, self.template_name, {'form': PaymentForm()})
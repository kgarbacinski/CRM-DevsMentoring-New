from CRM_core.models import Student
from dateutil.relativedelta import relativedelta
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class PaymentInfo(models.Model):
    student = models.OneToOneField(Student, on_delete=models.PROTECT, primary_key=True)
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=25)
    companyName = models.CharField(max_length=100, null=True, blank=True)
    nip = models.CharField(max_length=10, null=True, blank=True)
    street = models.CharField(max_length=200)
    postCode = models.CharField(max_length=6)
    town = models.CharField(max_length=20)
    country = models.CharField(max_length=20, default="Poland")
    phone = PhoneNumberField()
    email = models.EmailField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.student.__str__()


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    paymentDate = models.DateField()
    is_paid = models.BooleanField(default=False)

    @property
    def next_payment(self):
        return self.paymentDate + relativedelta(months=1)

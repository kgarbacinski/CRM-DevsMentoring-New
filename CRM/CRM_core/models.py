import uuid
from datetime import datetime
from decimal import Decimal

from dateutil import relativedelta
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Path(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(
        upload_to="user_avatar", default="user.png", null=True, blank=True
    )
    max_students = models.IntegerField(default=1)

    def count_all_meetings(self):
        current_hour = timezone.make_aware(
            datetime.now(), timezone.get_current_timezone()
        )
        return self.meeting_set.filter(date__lte=current_hour).count()

    def count_meetings_in_current_month(self):
        current_month = datetime.now().month
        return self.meeting_set.filter(date__month=current_month).count()

    def count_all_students(self):
        return self.student_set.count()

    def get_remaining_meetings(self):
        return 4 - self.count_all_meetings() % 4

    def save(self, *args, **kwargs):
        try:
            this = Mentor.objects.get(id=self.id)
            if this.user_image != self.user_image:
                this.user_image.delete(save=False)
        except ObjectDoesNotExist:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mentor = models.ManyToManyField(Mentor)
    enrollmentDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    path = models.ForeignKey(Path, on_delete=models.PROTECT)
    user_image = models.ImageField(
        upload_to="user_avatar", default="user.png", null=True, blank=True
    )
    no_month = models.IntegerField(default=1)

    def get_next_payment(self):
        if list(self.payment_set.all()):
            return list(self.payment_set.all())[-1].next_payment
        return "not paid"

    def count_all_meetings(self):
        current_hour = timezone.make_aware(
            datetime.now(), timezone.get_current_timezone()
        )
        return self.meeting_set.filter(date__lte=current_hour).count()

    def get_remaining_meetings(self):
        if self.is_sub_paid() is False:
            return 0
        return 4 - self.count_all_meetings() % 4

    def count_month_number(self):
        if self.count_all_meetings() % 4 == 0:
            self.no_month += 1

    def is_sub_paid(self):
        no_payments = self.payment_set.count()
        if self.no_month <= no_payments:
            return True
        return False

    def save(self, *args, **kwargs):
        try:
            this = Student.objects.get(id=self.id)
            if this.user_image != self.user_image:
                this.user_image.delete(save=False)
        except ObjectDoesNotExist:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

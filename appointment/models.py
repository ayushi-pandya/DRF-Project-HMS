from datetime import datetime
from django.db import models
from rest_framework.exceptions import ValidationError
from users.models import User, Staff


def date_validation(date):
    """
    function for date validation of appointment.
    """
    today = date.today()
    if date < today:
        raise ValidationError("The date cannot be in the past! Please select valid date.")
    return date


def timeslot_validation(time):
    """
    function for date validation of appointment.
    """
    today = datetime.now()
    if time < today:
        raise ValidationError("The time cannot be in the past! Please select valid time.")
    return time


class Appointments(models.Model):
    """
    This class is for creating table of appointment.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(validators=[date_validation])
    timeslot = models.CharField(max_length=200)
    disease = models.CharField(max_length=300)
    is_bill_generated = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f"Patient: {self.user} | Time: {self.timeslot}"

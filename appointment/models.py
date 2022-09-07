from datetime import datetime
from django.db import models
from rest_framework.exceptions import ValidationError
from users.models import User, Staff, Patient


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


class Room(models.Model):
    """
    class for creating table for rooms
    """
    ROOM_CHOICES = (
        ('General', 'General'),
        ('Private', 'Private'),
        ('Semi-Private', 'Semi-Private')
    )
    charge = models.IntegerField()
    AC = models.BooleanField(default=False)
    is_ICU = models.BooleanField(default=False)
    room_type = models.CharField(max_length=100, choices=ROOM_CHOICES)

    def __str__(self):
        return f"Room No:{self.id}"


class Admit(models.Model):
    """
    class for creating admit table
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ManyToManyField(Staff, through='AdmitStaff')
    disease = models.CharField(max_length=200)
    in_date = models.DateField(blank=False, validators=[date_validation])
    out_date = models.DateField(null=True)
    charge = models.IntegerField(null=True)
    is_bill_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.patient.username


class AdmitStaff(models.Model):
    """
    class for making through table for admit .
    """
    admit = models.ForeignKey(Admit, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return f"Staff:{self.staff}"


class Notification(models.Model):
    """
    class for creating notification module
    """
    patient = models.ForeignKey(Admit, on_delete=models.CASCADE)
    discharge = models.BooleanField(default=False)

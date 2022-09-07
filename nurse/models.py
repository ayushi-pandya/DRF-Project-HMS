from django.db import models

from appointment.models import Admit
from users.models import Staff


class NurseDuty(models.Model):
    """
    class for creating table of nurse duty.
    """
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    patient = models.ManyToManyField(Admit)

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Staff, User, Patient


@receiver(post_save, sender=User)
def create_staff(sender, instance, created, **kwargs):
    if created:
        if str(instance.role) == 'Doctor':
            staff = Staff.objects.create(staff=instance)
            staff.save()
        elif str(instance.role) == 'Patient':
            patient = Patient.objects.create(patient=instance)
            patient.save()

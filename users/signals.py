from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Staff


@receiver(post_save, sender=User)
def create_staff(sender, instance, created, **kwargs):
    print(1234567890)
    if created:
        print('abcd')
        Staff.objects.create(staff=instance)


@receiver(post_save, sender=User)
def save_staff(sender, instance, **kwargs):
    print(987654321)
    instance.staff.save()

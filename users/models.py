from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
import uuid


def validate_age(age):
    """
    function for age validation of users.
    """
    if age < 21:
        raise ValidationError('Please enter age above 21')


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, phone, age, address, gender, role, password=None, password2=None):
        """
        Creates and saves a User with the given email, phone, age, address, gender, role, profile and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email')

        if not phone:
            raise ValueError('Users must have phone number')

        if not age:
            raise ValueError('Users must have age')

        if not address:
            raise ValueError('Users must have address')

        if not gender:
            raise ValueError('Users must have gender')

        if not role:
            raise ValueError('Users must have role')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            age=age,
            address=address,
            gender=gender,
            role=role,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, age, address, gender, password=None):
        """
        Creates and saves a superuser with the given email, phone, age, address, gender, role, profile and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            age=age,
            address=address,
            gender=gender,
            role=UserRole.objects.get(id=1),
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserRole(models.Model):
    """
    class for creating table of role in hospital
    """
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


# custom user model
class User(AbstractBaseUser):
    """
    model for custom user table.
    """
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=255, verbose_name='Email', unique=True)
    phone = PhoneNumberField(help_text='Please use following format for phone number: +917834442134')
    age = models.IntegerField(validators=[validate_age])
    address = models.CharField(max_length=300)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    role = models.ForeignKey('UserRole', on_delete=models.CASCADE)
    profile = models.ImageField(default='default.jpg', upload_to='profile_pic/', null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'age', 'address', 'gender', 'role']

    def __str__(self):
        return f"User:{self.username}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class StaffSpeciality(models.Model):
    """
    create class for adding speciality table for staff.
    """
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return f"Staff Speciality:{self.speciality}"


class Staff(models.Model):
    """
    class for creating staff table.
    """
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    is_approve = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    speciality = models.ForeignKey('StaffSpeciality', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Staff Name:{self.staff.username}"


class Patient(models.Model):
    """
    class for making patient table.
    """
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    UUID = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Patient:{self.patient.username}"


class Medicine(models.Model):
    """
    class for creating table for medicine
    """
    medicine_name = models.CharField(max_length=200)
    charge = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Medicine Name:{self.medicine_name}"


class Prescription(models.Model):
    """
    class for creating table of patient's prescription
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    medicine = models.ManyToManyField(Medicine, through='PrescribeMedicine')

    def __str__(self):
        return f"patient:{self.patient.patient.username}"


class PrescribeMedicine(models.Model):
    """
    class for creating through table for prescription
    """
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"count:{self.count}"


class Emergency(models.Model):
    """
    class for creating emergency table
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    disease = models.CharField(max_length=500)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    is_bill_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"Patient:{self.patient.patient.username}"

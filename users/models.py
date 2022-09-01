from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError


def validate_age(age):
    """
    function for age validation of users.
    """
    if age < 21:
        raise ValidationError('Please enter age above 21')


class UserRole(models.Model):
    """
    class for creating table of role in hospital
    """
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


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
        return self.username

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
        return self.speciality

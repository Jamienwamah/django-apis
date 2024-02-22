from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
import uuid


class CustomAppUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ( 1, 'Male'),
        ( 2, 'Female'),
    ]
    id = models.CharField(primary_key=True, max_length=32, editable=False)  # Custom ID field
    first_name = models.CharField(max_length=255, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=255, verbose_name=_('Last Name'))
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    verification_code = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    phone_number_regex = RegexValidator(
        regex=r'^\+?234?\d{10}$', message=_("Phone number must be entered in the format: +234XXXXXXXXXX."))
    phone_number = models.CharField(validators=[
        phone_number_regex], max_length=15, unique=True, verbose_name=_('Phone Number'), blank=True)
    date_of_birth = models.DateField(
        verbose_name=_('Date of Birth'), null=True, blank=True)
    password = models.CharField(
        max_length=255, verbose_name=_('Password'), blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    residential_address = models.TextField(
        verbose_name=_('Residential Address'), blank=True)
    referral_code = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Referral Code'))
    wallet_address = models.CharField(
        max_length=36, blank=True, null=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    groups = models.ManyToManyField(Group, related_name='rent_customappuser_groups', blank=True)


    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_app_user_permissions', blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.id:  # Generate ID if not provided
            self.id = self.generate_custom_id()
        super().save(*args, **kwargs)

    def generate_custom_id(self):
        # Generate a UUID and manipulate it to match the desired format
        unique_id = uuid.uuid4().hex
        formatted_id = f"{unique_id[:6]}{unique_id[10:14]}{unique_id[18:22]}"
        return formatted_id
    
    def to_dict(self):
        # Return a dictionary containing field names and values of the User instance
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'verification_code': self.verification_code,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth,
            'password': self.password,
            'gender': self.gender,
            'residential_address': self.residential_address,
            'referral_code': self.referral_code
        }

    

    def __str__(self):
        return self.username
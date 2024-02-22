from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token
from rent.models import User
import uuid


class AccountUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]
    STATUS_CHOICES = [
        ('verified', _('Verified')),
        ('unverified', _('Unverified')),
        ('suspended', _('Suspended')),
        ('locked', _('Locked')),
    ]
    BOOL_CHOICES = [
        ('true', _('True')),
        ('false', _('False')),
    ]
    rent_user = models.ForeignKey("rent.User", on_delete=models.CASCADE)
    # AES key for encryption/decryption
    aes_key = models.CharField(max_length=32)
    # JWT secret key for token signing
    jwt_secret_key = models.CharField(max_length=64, default='')

    user_identifier = models.OneToOneField(
        "rent.User", on_delete=models.CASCADE, related_name='account_user')
    account_date = models.DateField(verbose_name=_(
        'Account Date'), null=True, default=None)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(
        max_length=255, blank=True, null=True, unique=True)
    bvn = models.CharField(max_length=255, blank=True, unique=True)
    card_cvv = models.CharField(max_length=6, blank=True)
    card_digit = models.PositiveIntegerField(default=None)
    card_expiry_date = models.DateField(verbose_name=_(
        'Card_Expiry Date'), null=True, default=None)
    card_holder_name = models.CharField(
        max_length=255, blank=True, unique=True)
    date_of_birth = models.DateField(verbose_name=_(
        'Date of Birth'), null=True, default=None)
    dva_creation_date = models.DateField(verbose_name=_(
        'Dva_Creation Date'), null=True, default=None)
    dva_name = models.CharField(max_length=255, blank=True, null=True)
    dva_number = models.CharField(max_length=255, blank=True, null=True)
    dva_username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    verification_code = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    finance_health = models.CharField(max_length=1, default=None)
    first_name = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    residential_address = models.TextField(
        verbose_name=_('Residential Address'), blank=True)
    has_dva = models.CharField(
        max_length=10, choices=BOOL_CHOICES, blank=True, null=True)
    has_rent = models.CharField(
        max_length=10, choices=BOOL_CHOICES, blank=True, null=True)
    has_verified_email = models.CharField(
        max_length=10, choices=BOOL_CHOICES, blank=True, null=True)
    has_verified_kyc = models.CharField(
        max_length=10, choices=BOOL_CHOICES, blank=True, null=True)
    has_verified_phone = models.CharField(
        max_length=10, choices=BOOL_CHOICES, blank=True, null=True)

    phone_number_regex = RegexValidator(
        regex=r'^\+?234?\d{10}$', message=_("Phone number must be entered in the format: +234XXXXXXXXXX.")
    )
    phone_number = models.CharField(validators=[
                                    phone_number_regex], max_length=15, unique=True, verbose_name=_('Phone Number'))

    user_id = models.CharField(max_length=255, blank=True, null=True)
    id_card = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='profile_images/', blank=True, null=True)
    kyc_details = models.TextField(blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    loan_amount = models.PositiveIntegerField(default=None)
    password = models.CharField(max_length=128)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    referrals = models.PositiveIntegerField(default=None)
    rentspace_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    total_assets = models.PositiveIntegerField(default=None)
    total_debts = models.PositiveIntegerField(default=None)
    total_savings = models.PositiveIntegerField(default=None)
    space_points = models.PositiveIntegerField(default=None)
    wallet_balance = models.PositiveIntegerField(default=None)
    wallet_id = models.CharField(max_length=255, blank=True, null=True)
    transaction_pin = models.CharField(max_length=6, unique=True)
    utility_points = models.PositiveIntegerField(default=0)
    wallet_address = models.CharField(max_length=255, default=None)

    groups = models.ManyToManyField(
        Group, related_name='user_account_accountuser_groups', blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='user_account_accountuser_user_permissions'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.wallet_address:
                self.wallet_address = self.generate_wallet_address()

        super().save(*args, **kwargs)

    def generate_wallet_address(self):
        unique_id = uuid.uuid4().hex
        wallet_address = f"{unique_id[:10]}-{unique_id[10:16]}"
        return wallet_address

    def clean(self):
        super().clean()
        if not self.is_adult():
            raise ValidationError(
                {'date_of_birth': _('User must be 18 years or older.')})

    def is_adult(self):
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - \
            ((today.month, today.day) <
             (self.date_of_birth.month, self.date_of_birth.day))
        return age >= 18

    def __str__(self):
        return self.username

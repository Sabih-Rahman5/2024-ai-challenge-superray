from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator




# user manager model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)




# Create your models here.

class CustomUser(AbstractUser):
    objects = CustomUserManager()


    PHONE_NUMBER_REGEX = r'^\+?1?\d{9,15}$'
    phone_number = models.CharField(max_length=17, blank=True, null=True, validators=[RegexValidator(regex=PHONE_NUMBER_REGEX)])

    # Choices for user type
    USER_TYPE_CHOICES = (
        ('RESEARCHER', 'Researcher'),
        ('HEALTH_CARE_PROFESSIONAL', 'Health Care Professional'),
        ('STANDARD_USER', 'Standard User'),
    )

    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, default='STANDARD_USER')

    # Additional fields
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)

    def __str__(self) -> str:
        return f'ID: {self.id} {self.username}'


#report model

class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    comparisons = models.TextField(blank=True)
    indication = models.CharField(max_length=255, blank=True)
    findings = models.TextField(blank=True)
    impression = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'Report ID: {self.id}'
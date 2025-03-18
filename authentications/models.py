from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable
from .utils import CustomUserManager
from django_countries.fields import CountryField

# Create your models here.
    
class CustomUser(AbstractUser): # Add this class for custom user model
    username = None # Remove the username field. We will use email for authentication.    
    email = models.EmailField(unique=True)
    mobile = models.CharField(unique=True, null=True, blank=True, max_length=15)
    address = models.CharField(null= True, blank=True, max_length=100)   
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    #country = models.CharField(blank=True, max_length=20)
    country = CountryField(blank_label="(Select country)")
    postal_code = models.CharField(blank=True, max_length=10)
    profile_picture = models.ImageField(null= True, blank=True, upload_to='userprofile')
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email' # Use email as the unique identifier
    REQUIRED_FIELDS = []    # Remove the username as required field. We will use email for authentication.

    objects = CustomUserManager()

    def __str__(self):
        return self.email
  
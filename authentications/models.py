from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable
from .utils import CustomUserManager

# Create your models here.
    
class CustomUser(AbstractUser): # Add this class for custom user model
    username = None # Remove the username field. We will use email for authentication.    
    email = models.EmailField(unique=True)
    mobile = models.CharField(unique=True, null=True, blank=True, max_length=15)
    address = models.CharField(null= True, blank=True, max_length=100)   
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    profile_picture = models.ImageField(null= True, blank=True, upload_to='userprofile')
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email' # Use email as the unique identifier
    REQUIRED_FIELDS = []    # Remove the username as required field. We will use email for authentication.

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
    
    
    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         print(self.password)
    #         #self.set_password(self.password)
    #         if not is_password_usable(self.password):
    #             self.password = make_password(self.password)
    #         else:
    #             self.password = make_password(self.password)
    #             print('Password is already hashed')
                
    #     super().save(*args, **kwargs)
    
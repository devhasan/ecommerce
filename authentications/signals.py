""" Create a signal to automatically create a UserProfile when a CustomUser is created: """

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def create_custom_user(sender, instance, created, **kwargs):
#     if created:
#         CustomUser.objects.create(user=instance)

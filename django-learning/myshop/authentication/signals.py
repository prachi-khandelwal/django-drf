# signals.py - Signal receivers for the authentication app

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
import logging

# Get a logger for this module
logger = logging.getLogger('django')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created.
    This ensures every user has a profile.
    
    Note: We don't need a separate save_user_profile signal because:
    - The profile is created automatically on user creation
    - If you modify profile data, you should save it explicitly in your code
    - Automatically saving on every User save can cause unnecessary DB writes
    """
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f"👤 Auto-created profile for user: {instance.username}")


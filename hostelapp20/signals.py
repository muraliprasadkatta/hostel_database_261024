# <your_app>/signals.py

from django.dispatch import receiver
from social_django.models import UserSocialAuth
from social_core.signals import social_user_authenticated

@receiver(social_user_authenticated)
def social_user_authenticated(sender, request, socialuser, **kwargs):
    print(f"Authenticated via {socialuser.provider}")
    if socialuser.provider == 'google-oauth2':
        user = socialuser.user
        user.customuser.registration_method = 'Google'
        user.customuser.save()

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from .models import TechUserProfile


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    This class overrides the default social login functionality
    of all auth so I can associate an existing record with a 
    social account. It also adds the tech user profile to the
    user if they are a new user.
    """

    def pre_social_login(self, request, sociallogin):
        User = get_user_model()
        email = sociallogin.account.extra_data.get('email')
        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if sociallogin.is_new:
            TechUserProfile.objects.create(user=user)
        return user

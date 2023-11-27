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

        github_name = sociallogin.account.extra_data.get('name', '')

        if github_name:
            try:
                github_name = github_name.split(' ')
                first_name = github_name[0]
                last_name = github_name[-1]
                user.first_name = first_name
                user.last_name = last_name
                user.work_title = ''
                user.save()
            except Exception as e:
                print("Error updating user name:", e)
        else:
            user.first_name = "New"
            user.last_name = "User"
            user.work_title = ''
            user.save()

        github_username = sociallogin.account.extra_data.get('login', '')

        try:
            tech_profile = TechUserProfile.objects.create(
                user=user,
                github_username=github_username,
                seeking_employment=False
            )
        except Exception as e:
            print("Error creating TechUserProfile:", e)

        return user

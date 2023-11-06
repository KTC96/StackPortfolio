from allauth.account.forms import SignupForm
from django import forms
from .models import TechUserProfile, RecruiterUserProfile


class CustomUserForm(SignupForm):
    """
    Create a custom signup form that extends SignupForm.
    """
    first_name = forms.CharField(max_length=40, label='First Name')
    last_name = forms.CharField(max_length=40, label='Last Name')
    town_city = forms.CharField(
        max_length=85, label='Town/City', required=False)
    display_town_city = forms.BooleanField(
        required=False, label='Display Town/City', initial=False)
    country = forms.CharField(max_length=60, label='Country', required=False)
    display_email = forms.BooleanField(
        required=False, label='Display Email', initial=False)
    website = forms.URLField(required=False, label='Website')
    phone_number = forms.CharField(
        max_length=20, required=False, label='Phone Number')
    display_phone_number = forms.BooleanField(
        required=False, initial=False, label='Display Phone Number')
    profile_image = forms.URLField(required=False, label='Profile Image')
    bio = forms.CharField(widget=forms.Textarea,
                          required=False, label='Bio', max_length=500)
    work_title = forms.CharField(
        max_length=80, required=False, label='Title', help_text='e.g. Software Engineer')
    company = forms.CharField(max_length=80, required=False, label='Company')
    linkedin_username = forms.CharField(
        max_length=80, required=False, label='LinkedIn Username')
    twitter_handle = forms.CharField(
        max_length=80, required=False, label='Twitter Handle')

    def save(self, request):
        user = super(CustomUserForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.town_city = self.cleaned_data['town_city']
        user.display_town_city = self.cleaned_data.get(
            'display_town_city', False)
        user.country = self.cleaned_data['country']
        user.display_email = self.cleaned_data.get('display_email', False)
        user.website = self.cleaned_data['website']
        user.phone_number = self.cleaned_data['phone_number']
        user.display_phone_number = self.cleaned_data.get(
            'display_phone_number', False)
        user.profile_image = self.cleaned_data['profile_image']
        user.bio = self.cleaned_data['bio']
        user.work_title = self.cleaned_data['work_title']
        user.company = self.cleaned_data['company']
        user.linkedin_username = self.cleaned_data['linkedin_username']
        user.twitter_handle = self.cleaned_data['twitter_handle']

        user.save()
        return user


class TechUserForm(CustomUserForm):
    """
    This form is for users who are signing up as tech users.
    """
    github_username = forms.CharField(
        max_length=40, required=False, label='GitHub Username')
    seeking_employment = forms.BooleanField(
        required=False, initial=False, label='Seeking Employment')

    def save(self, request):

        user = super(TechUserForm, self).save(request)

        tech_user_profile = TechUserProfile(
            user=user,
            github_username=self.cleaned_data.get('github_username', ''),
            seeking_employment=self.cleaned_data.get(
                'seeking_employment', False),
        )
        tech_user_profile.save()

        return user


class RecruiterUserForm(CustomUserForm):
    """
    This form is used to sign up recruiter users.
    """

    def save(self, request):
        user = super(RecruiterUserForm, self).save(request)

        recruiter_user_profile = RecruiterUserProfile(user=user)
        recruiter_user_profile.save()

        return user

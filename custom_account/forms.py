from allauth.account.forms import SignupForm
from django import forms
from .models import TechUserProfile, RecruiterUserProfile, CustomUser


class CustomUserForm(SignupForm):
    """
    Create a custom signup form that extends SignupForm.
    """
    first_name = (
        forms.CharField(
            max_length=40,
            min_length=2,
            label='First Name',
            required=True,
            help_text='Required',
            widget=forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    last_name = (
        forms.CharField(
            max_length=40,
            min_length=2,
            label='Last Name',
            required=True,
            help_text='Required',
            widget=forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    email = (
        forms.EmailField(
            max_length=60,
            label='Email',
            required=True,
            help_text='Required',
            widget=forms.EmailInput(
                attrs={
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))

    display_email = forms.BooleanField(
        required=False,
        label='Display Email',
        initial=False,
        help_text='Email will be displayed on your profile',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0 w-50',
                'checked': ''}
        ))
    username = (
        forms.CharField(
            max_length=40,
            min_length=5,
            label='Username',
            required=True,
            help_text='This will be for your profile URL',
            widget=forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    password1 = (
        forms.CharField(
            max_length=40,
            min_length=8,
            label='Password',
            required=True,
            help_text='Required',
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))

    password2 = (
        forms.CharField(
            max_length=40,
            min_length=8,
            label='Confirm Password',
            required=True,
            help_text='Required',
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))

    town_city = forms.CharField(
        max_length=85,
        label='Town/City',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        ))

    display_town_city = forms.BooleanField(
        required=False, label='Display Town/City',
        initial=False,
        help_text='Town/City will be displayed on your profile',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0',
                'checked': ''
            }
        ))

    country = forms.CharField(
        max_length=60,
        label='Country',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    website = forms.URLField(
        required=False,
        label='Website',
        help_text='e.g. https://www.stackportfolio.com',
        widget=forms.URLInput(
            attrs={
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label='Phone Number',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    display_phone_number = forms.BooleanField(
        required=False,
        initial=False,
        label='Display Phone Number',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0',
                'checked': ''
            }
        )
    )

    profile_image = forms.ImageField(
        required=False,
        label='Profile Image',
        help_text='Upload a profile image',
        widget=forms.FileInput(
            attrs={
                'class': """
                file-input file-input-bordered
                file-input-primary w-full mt-3
                """
            }
        )
    )

    bio = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'textarea textarea-bordered textarea-secondary w-full',
            'placeholder': 'Write a short bio for your profile'
        }
    ),
        required=False,
        label='Bio',
        max_length=500
    )

    work_title = forms.CharField(
        max_length=80,
        required=False,
        label='Title',
        help_text='e.g. Software Engineer',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    company = forms.CharField(
        max_length=80,
        required=False,
        label='Company',
        help_text='e.g. Stack Portfolio',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    linkedin_username = forms.CharField(
        max_length=80,
        required=False,
        label='LinkedIn Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    twitter_handle = forms.CharField(
        max_length=80,
        required=False,
        label='Twitter Handle',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

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
        max_length=40,
        required=False,
        label='GitHub Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    seeking_employment = forms.BooleanField(
        required=False,
        initial=False,
        label='Seeking Employment',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0',
                'checked': ''
            }
        )
    )

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


class CustomUserEditForm(forms.ModelForm):
    """
    This form is required to edit the user profile.
    """
    first_name = (
        forms.CharField(
            max_length=40,
            min_length=2,
            label='First Name',
            required=True,
            help_text='Required',
            widget=forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    last_name = (
        forms.CharField(
            max_length=40,
            min_length=2,
            label='Last Name',
            required=True,
            help_text='Required',
            widget=forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    email = (
        forms.EmailField(
            max_length=60,
            label='Email',
            required=True,
            help_text='Required',
            widget=forms.EmailInput(
                attrs={
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    display_email = forms.BooleanField(
        required=False,
        label='Display Email',
        initial=False,
        help_text='Email will be displayed on your profile',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0 w-50',
                'checked': ''}
        ))
    username = (
        forms.CharField(
            max_length=40,
            min_length=5,
            label='Username',
            required=True,
            help_text='This will be for your profile URL',
            widget=forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    password1 = (
        forms.CharField(
            max_length=40,
            min_length=8,
            label='Password',
            required=True,
            help_text='Required',
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    password2 = (
        forms.CharField(
            max_length=40,
            min_length=8,
            label='Confirm Password',
            required=True,
            help_text='Required',
            widget=forms.PasswordInput(
                attrs={
                    'placeholder': '',
                    'class': 'input input-bordered input-secondary w-full'
                }
            )))
    town_city = forms.CharField(
        max_length=85,
        label='Town/City',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        ))
    display_town_city = forms.BooleanField(
        required=False, label='Display Town/City',
        initial=False,
        help_text='Town/City will be displayed on your profile',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0',
                'checked': ''
            }
        ))
    country = forms.CharField(
        max_length=60,
        label='Country',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )
    website = forms.URLField(
        required=False,
        label='Website',
        help_text='e.g. https://www.stackportfolio.com',
        widget=forms.URLInput(
            attrs={
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label='Phone Number',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )
    display_phone_number = forms.BooleanField(
        required=False,
        initial=False,
        label='Display Phone Number',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0',
                'checked': ''
            }
        )
    )

    profile_image = forms.ImageField(
        required=False,
        label='Profile Image',
        help_text='Upload a profile image',
        widget=forms.FileInput(
            attrs={
                'class': """
                file-input file-input-bordered
                file-input-primary w-full mt-3
                """
            }
        )
    )

    bio = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'textarea textarea-bordered textarea-secondary w-full',
            'placeholder': 'Write a short bio for your profile'
        }
    ),
        required=False,
        label='Bio',
        max_length=500
    )

    work_title = forms.CharField(
        max_length=80,
        required=False,
        label='Title',
        help_text='e.g. Software Engineer',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    company = forms.CharField(
        max_length=80,
        required=False,
        label='Company',
        help_text='e.g. Stack Portfolio',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    linkedin_username = forms.CharField(
        max_length=80,
        required=False,
        label='LinkedIn Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    twitter_handle = forms.CharField(
        max_length=80,
        required=False,
        label='Twitter Handle',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    class Meta:
        """
        Meta to specify the model and fields to be used.
        """
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'town_city',
            'display_town_city',
            'country',
            'display_email',
            'website',
            'phone_number',
            'display_phone_number',
            'profile_image',
            'bio',
            'work_title',
            'company',
            'linkedin_username',
            'twitter_handle'
        ]


class TechUserProfileEditForm(forms.ModelForm):
    """
    TechUser update form.
    """
    github_username = forms.CharField(
        max_length=40,
        required=False,
        label='GitHub Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'input input-bordered input-secondary w-full'
            }
        )
    )

    seeking_employment = forms.BooleanField(
        required=False,
        initial=False,
        label='Seeking Employment',
        help_text='Are you currently seeking a new role?',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'toggle toggle-secondary mt-3 lg:mt-0',
                'checked': ''
            }
        )
    )

    class Meta:
        """
        Meta to specify the model and fields to be used.
        """
        model = TechUserProfile
        fields = ['github_username', 'seeking_employment']


class RecruiterUserProfileEditForm(forms.ModelForm):
    """
    RecruiterUser update form.
    """
    class Meta:
        """
        Meta to specify the model and fields to be used.
        """
        model = RecruiterUserProfile
        fields = []

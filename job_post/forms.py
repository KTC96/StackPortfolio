from django import forms
from .models import JobPost
from work_location_type.models import WorkLocationType


class JobPostForm(forms.ModelForm):
    """
    This is a form for the job post model. It also
    gets the tech so that it can be used when creating
    anew job post.
    """
    class Meta:
        model = JobPost
        fields = ('name',
                  'description',
                  'active',
                  'company',
                  'location',
                  'work_location_type',
                  'salary_from',
                  'salary_to',
                  'salary_currency',
                  'technologies'
                  )


class CustomJobPostForm(forms.ModelForm):
    """
    This is a form for the job post model. It also
    gets the tech so that it can be used when creating
    anew job post. The custom form overrides the
    default many to many output for work location type.
    """

    # using the choiceField for a radio button where
    # choices are the work location types in the database
    work_location_type = forms.ModelChoiceField(
        queryset=WorkLocationType.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
        required=True
    )

    class Meta:
        model = JobPost
        fields = ('name',
                  'description',
                  'active',
                  'company',
                  'location',
                  'work_location_type',
                  'salary_from',
                  'salary_to',
                  'salary_currency',
                  'technologies'
                  )

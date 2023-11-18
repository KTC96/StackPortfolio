from django import forms
from .models import JobPost


class JobPostForm(forms.ModelForm):
    """
    This is a form for the project model. It also
    gets the tech_dataset so that the many to many
    field can be a datalist in the template.
    """
    class Meta:
        model = JobPost
        fields = ('name',
                  'description',
                  'active',
                  'company',
                  'location',
                  'salary_from',
                  'salary_to',
                  'salary_currency',
                  'technologies'
                  )

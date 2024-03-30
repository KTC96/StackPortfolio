from django import forms
from .models import Project
from technology.models import Tech


class ProjectForm(forms.ModelForm):
    """
    This is a form for the project model. It also
    gets the tech_dataset so that the many to many
    field can be a datalist in the template.
    """
    class Meta:
        model = Project
        fields = ('name',
                  'contributors',
                  'description',
                  'image',
                  'active',
                  'github_repo_url',
                  'deployed_url',
                  'technologies'
                  )

from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name',
                  'project_description',
                  'project_image',
                  'project_active',
                  'github_repo_url',
                  'deployed_url',
                  'technologies'
                  )

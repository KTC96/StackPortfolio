from django.shortcuts import render
from django.views.generic import DetailView
from .models import Project


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_page.html'
    slug_field = 'project_slug'
    slug_url_kwarg = 'project_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(
            project_slug=self.kwargs['project_slug'])
        return context

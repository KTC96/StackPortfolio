from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Project


class ProjectDetailView(DetailView):
    """
    This view handles the displaying of a
    single project on its own page.
    """
    model = Project
    template_name = 'project_page.html'
    slug_field = 'project_slug'
    slug_url_kwarg = 'project_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(
            project_slug=self.kwargs['project_slug'])
        return context


class ProjectListView(ListView):
    """
    This view lists all the projects on the
    a project list page.
    """
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        """
        Returns all the projects.
        """
        return Project.objects.filter(project_active=True).order_by('-project_date_created')

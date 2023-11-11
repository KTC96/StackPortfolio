from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from .models import Project
from .forms import ProjectForm
from custom_account.models import CustomUser


class ProjectDetailView(DetailView):
    """
    This view handles the displaying of a
    single project on its own page.
    """
    model = Project
    template_name = 'project_page.html'
    slug_field = 'project_slug'
    slug_url_kwarg = 'project_slug'

    def get_object(self):
        """
        Returns the project object based on the project_slug and user slug.
        """
        project_slug = self.kwargs['project_slug']
        user_slug = self.kwargs.get('slug')
        user = get_object_or_404(CustomUser, slug=user_slug)
        return get_object_or_404(Project, project_slug=project_slug, user=user)

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)
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


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    Class to handle project creation.
    """
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.slug == self.kwargs['slug']:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account_login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'slug': self.request.user.slug})

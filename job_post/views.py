from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import JobPost
from custom_account.models import CustomUser


class JobPostDetailView(DetailView):
    """
    This view handles the displaying of a
    single project on its own page.
    """
    model = JobPost
    template_name = 'job_post_page.html'
    context_object_name = 'job_post'

    def get_object(self):
        """
        Returns the project object based on the project_slug and user slug.
        """
        job_post_id = self.kwargs.get('id')
        user_slug = self.kwargs.get('slug')
        user = get_object_or_404(CustomUser, slug=user_slug)
        return get_object_or_404(JobPost, user=user, id=job_post_id)

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)
        return context


class JobPostListView(ListView):
    """
    This view lists all the projects on the
    a project list page.
    """
    model = JobPost
    template_name = 'job_post_list.html'
    context_object_name = 'job_posts'
    paginate_by = 9

    def get_queryset(self):
        """
        Returns all the projects.
        """
        return JobPost.objects.filter(
            active=True).order_by('-date_created')

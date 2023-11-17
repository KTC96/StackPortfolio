from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import JobPost


class JobPostListView(ListView):
    """
    This view lists all the projects on the
    a project list page.
    """
    model = JobPost
    template_name = 'job-post-list.html'
    context_object_name = 'job_posts'
    paginate_by = 9

    def get_queryset(self):
        """
        Returns all the projects.
        """
        return JobPost.objects.filter(
            active=True).order_by('-date_created')

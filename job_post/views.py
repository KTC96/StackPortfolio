from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import JobPost
from .forms import JobPostForm
from custom_account.models import CustomUser
from technology.models import Tech


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


class JobPostCreateView(LoginRequiredMixin, CreateView):
    """
    Class to handle project creation.
    """
    model = JobPost
    form_class = JobPostForm
    template_name = 'create_job_post.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.slug == self.kwargs['slug']:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_technologies'] = Tech.objects.all().filter(
            is_approved=True)
        return context

    def form_valid(self, form):
        job_post = form.save(commit=False)
        job_post.user = self.request.user
        job_post.save()

        # Add existing technologies
        existing_tech_ids = form.cleaned_data.get('technologies')
        for tech_id in existing_tech_ids:
            job_post.technologies.add(tech_id)

        # If a tech is submitting and it's not
        # in the database, add it to the database
        # as unapproved.
        new_tech_names = self.request.POST.get(
            'new_technologies', '').split(',')
        for tech_name in new_tech_names:
            tech_name = tech_name.strip()
            if tech_name:
                tech = Tech.objects.get_or_create(
                    tech_name=tech_name, defaults={'is_approved': False})
                job_post.technologies.add(tech)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'user_profile', kwargs={
                'slug': self.request.user.slug})

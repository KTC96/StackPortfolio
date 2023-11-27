from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import JobPost
from .forms import CustomJobPostForm
from custom_account.models import CustomUser
from technology.models import Tech


class JobPostDetailView(DetailView):
    """
    This view handles the displaying of a
    single job_post on its own page.
    """
    model = JobPost
    template_name = 'job_post_page.html'
    context_object_name = 'job_post'

    def get_object(self):
        """
        Returns the job_post object based on the job_post_id and user slug.
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
        context['selected_work_location_type'] = self.object.work_location_type.all(
        )[0]
        return context


class JobPostListView(ListView):
    """
    This view lists all the job posts on the
    a job post list page.
    """
    model = JobPost
    template_name = 'job_post_list.html'
    context_object_name = 'job_posts'
    paginate_by = 9

    def get_queryset(self):
        """
        Returns all the job posts.
        """
        return JobPost.objects.filter(
            active=True).order_by('-date_created')


class JobPostCreateView(LoginRequiredMixin, CreateView):
    """
    Class to handle job_post creation.
    """
    model = JobPost
    form_class = CustomJobPostForm
    template_name = 'create_job_post.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the user is logged in and if the user
        is the same as the user in the url.
        If not, redirect to the account login page.
        """
        if request.user.is_authenticated and request.user.slug == self.kwargs['slug']:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account_login')

    def get_context_data(self, **kwargs):
        """
        Passes all the approved technologies to the template.
        """
        context = super().get_context_data(**kwargs)
        context['all_technologies'] = Tech.objects.all().filter(
            is_approved=True)
        return context

    def form_valid(self, form):
        """
        Handles the form validation and saving.
        """
        job_post = form.save(commit=False)
        job_post.user = self.request.user
        job_post.save()

        # Add existing technologies
        existing_tech_ids = form.cleaned_data.get('technologies')
        for tech_id in existing_tech_ids:
            job_post.technologies.add(tech_id)

        # If a tech is submitted and it's not
        # in the database, add it to the database
        # as unapproved.
        new_tech_names = self.request.POST.get(
            'new_technologies', '').split(',')
        for tech_name in new_tech_names:
            tech_name = tech_name.strip()
            if tech_name:
                tech, created = Tech.objects.get_or_create(
                    tech_name=tech_name, defaults={'is_approved': False})
                job_post.technologies.add(tech)

        selected_work_location_type_id = form.cleaned_data['work_location_type']
        job_post.work_location_type.clear()
        job_post.work_location_type.add(
            selected_work_location_type_id)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Redirect to the user profile page after
        successful job post creation.
        """
        return reverse_lazy(
            'user_profile', kwargs={
                'slug': self.request.user.slug})


class JobPostEditView(LoginRequiredMixin, UpdateView):
    """
    This class handles making updates to the job_post.
    """
    model = JobPost
    form_class = CustomJobPostForm
    template_name = 'edit_job_post.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def get_object(self, queryset=None):
        """
        Returns the job_post object based on the job_post_id.
        """
        id = self.kwargs.get('id')
        return get_object_or_404(JobPost, id=id)

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the user is logged in and if the user
        is the same as the user in the url.
        If not, redirect to the account login page.
        """
        job_post = self.get_object()
        if request.user.is_authenticated and request.user == job_post.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, "You do not have permission to edit this job post.")
            return redirect('account_login')

    def get_context_data(self, **kwargs):
        """
        Passed the job_post object and all the approved technologies
        to the template.
        """
        context = super().get_context_data(**kwargs)
        context['job_post'] = self.object
        context['all_technologies'] = Tech.objects.all().filter(
            is_approved=True)
        context['job_post_technologies'] = self.object.technologies.all()
        context['job_post_work_location_type_ids'] = self.object.work_location_type.values_list(
            'id', flat=True)

        return context

    def remove_tech_from_job_post(self, job_post, tech_id):
        """
        Remove a tech from a job_post.
        """
        job_post.technologies.remove(tech_id)

    def form_valid(self, form):
        """
        Handles the form validation and saving.
        """
        job_post = form.save(commit=False)
        job_post.user = self.request.user
        job_post.save()

        # Add existing technologies and remove any that
        # were removed on the frontend
        existing_tech_ids = form.cleaned_data.get('technologies')
        job_post_tech_ids = job_post.technologies.values_list('id', flat=True)
        tech_to_remove = set(job_post_tech_ids) - set(existing_tech_ids)
        for tech in tech_to_remove:
            self.remove_tech_from_job_post(job_post, tech)
        for tech_id in existing_tech_ids:
            job_post.technologies.add(tech_id)

        # If a tech is submitted and it's not
        # in the database, add it to the database
        # as unapproved.
        new_tech_names = self.request.POST.get(
            'new_technologies', '').split(',')
        for tech_name in new_tech_names:
            tech_name = tech_name.strip()
            if tech_name:
                tech, created = Tech.objects.get_or_create(
                    tech_name=tech_name, defaults={'is_approved': False})
                job_post.technologies.add(tech)

        # So for the work location type, I needed to do some extra
        # work to get the radio button to display correctly. I had
        # to clear the existing selection and then pass in the single
        # selected work location type.
        selected_work_location_type_id = form.cleaned_data['work_location_type']
        job_post.work_location_type.clear()
        job_post.work_location_type.add(
            selected_work_location_type_id)

        return HttpResponseRedirect(self.get_success_url())


@login_required
@require_POST
def delete_job_post(request, slug, id):
    """
    Handles job post deletion.
    """
    user = request.user
    job_post = get_object_or_404(JobPost, id=id)

    if user == job_post.user:
        job_post.delete()
        messages.success(
            request, "Your job post has been successfully deleted.")
        return redirect(reverse('custom_account:user_profile', kwargs={'slug': slug}))

    messages.error(
        request, "You cannot delete this job post.")
    return redirect(reverse('custom_account:user_profile', kwargs={'slug': slug}))

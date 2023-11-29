
import random
from allauth.account.views import SignupView
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, UpdateView, DetailView
from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.text import slugify
import cloudinary.uploader
import cloudinary
from allauth.socialaccount import providers
from .forms import (CustomUserEditForm, TechUserForm,
                    RecruiterUserForm, TechUserProfileEditForm,
                    RecruiterUserProfileEditForm, UserSettingsForm
                    )
from .models import CustomUser
from project.models import Project


class IndexView(TemplateView):
    """
    To output users for testing on the homepage.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        valid_projects_id_list = Project.objects.filter(
            active=True,
            image__isnull=False).values_list(
            'id',
            flat=True)

        random_projects_id_list = random.sample(
            list(valid_projects_id_list), min(len(valid_projects_id_list), 6))

        query_set = Project.objects.filter(id__in=random_projects_id_list)

        context['users'] = CustomUser.objects.all()
        context['randomProjects'] = query_set
        return context


class TechUserSignupView(SignupView):
    """
    Form to process tech user signups.
    """
    template_name = 'account/signup-tech.html'
    form_class = TechUserForm
    redirect_field_name = 'next'
    view_name = 'techuser_signup'


class RecruiterUserSignupView(SignupView):
    """
    Form to process recruiter user signups.
    """
    template_name = 'account/signup-recruiter.html'
    form_class = RecruiterUserForm
    redirect_field_name = 'next'
    view_name = 'recruiteruser_signup'


class UserProfileDetailView(DetailView):
    """
    View to display user profiles.
    """
    model = CustomUser
    template_name = 'user_profile.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'tech_profile'):
            context['user_projects'] = self.object.projects.all()
        elif hasattr(self.object, 'recruiter_profile'):
            context['user_job_posts'] = self.object.job_posts.all()

        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    """
    This class handles updating the user profile details.
    """
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'account/user_edit_profile.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and
                request.user.slug == self.kwargs['slug']):
            messages.error(
                request, "You are not authorised to view this page.")
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'tech_profile'):
            context['tech_profile_form'] = TechUserProfileEditForm(
                instance=self.object.tech_profile
            )
            context['job_post_work_location_type_ids'] = (
                self.object.tech_profile.work_location_type.values_list(
                    'id', flat=True))
        elif hasattr(self.object, 'recruiter_profile'):
            context['recruiter_profile_form'] = RecruiterUserProfileEditForm(
                instance=self.object.recruiter_profile
            )

        context['user_projects'] = self.object.projects.all()
        return context

    def form_valid(self, form):
        current_profile = CustomUser.objects.get(pk=self.object.pk)
        old_image_public_id = None
        if 'profile_image' in form.changed_data:
            old_image_public_id = current_profile.profile_image.public_id

        response = super(UserProfileEditView, self).form_valid(form)

        if hasattr(self.object, 'tech_profile'):
            tech_profile_form = TechUserProfileEditForm(
                self.request.POST, instance=self.object.tech_profile)
            if tech_profile_form.is_valid():
                tech_profile_form.save()

        # Handle recruiter_profile_form only if the user has a recruiter_profile
        elif hasattr(self.object, 'recruiter_profile'):
            recruiter_profile_form = RecruiterUserProfileEditForm(
                self.request.POST, instance=self.object.recruiter_profile)
            if recruiter_profile_form.is_valid():
                recruiter_profile_form.save()

        if old_image_public_id:
            try:
                cloudinary.uploader.destroy(
                    old_image_public_id, invalidate=True)
            except Exception as e:
                print(f"Error deleting old photo: {e}")

        messages.success(
            self.request, "Profile successfully updated.")

        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error updating your profile.")
        return super(UserProfileEditView, self).form_invalid(form)

    def get_success_url(self):
        return reverse(
            'custom_account:user_profile', kwargs={
                'slug': self.object.slug})


class UserSettingsView(LoginRequiredMixin, UpdateView):
    """
    This class handles updating the user settings.
    """
    model = CustomUser
    form_class = UserSettingsForm
    template_name = 'user_settings.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and
                request.user.slug == self.kwargs['slug']):
            messages.error(
                request, "You are not authorised to view this page.")
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = self.object
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.username = form.cleaned_data['username']
        user.slug = slugify(user.username)
        user.save()

        messages.success(
            self.request, "Details successfully updated.")

        return super(UserSettingsView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error updating your details.")
        return super(UserSettingsView, self).form_invalid(form)

    def get_success_url(self):
        return reverse(
            'custom_account:user_profile', kwargs={
                'slug': self.object.slug})


@login_required
@require_POST
def delete_user(request, slug):
    user = request.user
    if user.slug == slug:
        if user.profile_image:
            photo_public_id = user.profile_image.public_id
            try:
                cloudinary.uploader.destroy(photo_public_id, invalidate=True)
            except Exception as e:
                print(f"Error deleting profile photo: {e}")

        try:
            if hasattr(user, 'tech_profile'):
                pass
        except CustomUser.tech_profile.RelatedObjectDoesNotExist:
            print("Tech profile not found or inaccessible.")

        try:
            if hasattr(user, 'recruiter_profile'):
                pass
        except CustomUser.recruiter_profile.RelatedObjectDoesNotExist:
            print("Recruiter profile not found or inaccessible.")

        user.delete()
        messages.success(
            request, "Your profile has been deleted.")
        return redirect(reverse('homepage'))

    messages.error(request, "You cannot delete this profile.")
    return redirect(reverse('custom_account:user_profile', kwargs={'slug': slug}))


class AccountTypeView(TemplateView):
    """
    Used to give the user signing up the option to choose.
    View is required to pass allauth social auth variables
    to the template.
    """
    template_name = 'account_type.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['socialaccount_providers'] = providers.registry.provider_map
        return context

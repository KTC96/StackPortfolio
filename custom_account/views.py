
import random
from allauth.account.views import SignupView
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import render, reverse, redirect
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import (CustomUserEditForm, TechUserForm,
                    RecruiterUserForm, TechUserProfileEditForm,
                    RecruiterUserProfileEditForm)
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
            project_active=True,
            project_image__isnull=False).values_list(
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
        if request.user.is_authenticated and request.user.slug == self.kwargs['slug']:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                "You are not allowed to view this page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'tech_profile'):
            context['tech_profile_form'] = TechUserProfileEditForm(
                instance=self.object.tech_profile
            )
        elif hasattr(self.object, 'recruiter_profile'):
            context['recruiter_profile_form'] = RecruiterUserProfileEditForm(
                instance=self.object.recruiter_profile
            )

        context['user_projects'] = self.object.projects.all()
        return context

    def form_valid(self, form):
        response = super(UserProfileEditView, self).form_valid(form)

        tech_profile_form = TechUserProfileEditForm(
            self.request.POST, instance=self.object.tech_profile)
        if tech_profile_form.is_valid():
            tech_profile_form.save()

        return response

    def get_success_url(self):
        return reverse('user_profile', kwargs={'slug': self.object.slug})


@login_required
@require_POST
def delete_user(request, slug):
    """
    Handles user deletion.
    """
    user = request.user
    if user.slug == slug:
        user.delete()
        messages.success(
            request, "Your profile has been successfully deleted.")
        return redirect(reverse('homepage'))

    messages.error(request, "You cannot delete this profile.")
    return redirect(reverse('user_profile', kwargs={'slug': slug}))

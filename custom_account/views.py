from allauth.account.views import SignupView
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import render, reverse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (CustomUserEditForm, TechUserForm,
                    RecruiterUserForm, TechUserProfileEditForm,
                    RecruiterUserProfileEditForm)
from .models import CustomUser


def index(request):
    """
    To output users for testing on the homepage.
    TODO: Remove this view.
    """
    users = CustomUser.objects.all()
    return render(request, 'index.html', {'users': users})


class IndexView(TemplateView):
    """
    To output users for testing on the homepage.
    TODO: Remove this view.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
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


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    """
    This class handles updating the user profile details.
    """
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'account/user_edit_profile.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

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

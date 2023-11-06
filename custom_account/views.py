from allauth.account.views import SignupView
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic import DetailView
from .forms import TechUserForm, RecruiterUserForm
from .models import CustomUser, TechUserProfile


def index(request):
    users = CustomUser.objects.all()
    return render(request, 'index.html', {'users': users})


class IndexView(TemplateView):
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

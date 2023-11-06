from allauth.account.views import SignupView
from .forms import TechUserForm, RecruiterUserForm


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

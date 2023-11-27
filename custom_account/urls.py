from django.urls import path, include
from .views import (TechUserSignupView,
                    RecruiterUserSignupView,
                    UserProfileDetailView,
                    UserProfileEditView,
                    UserSettingsView,
                    AccountTypeView,
                    delete_user,
                    )

app_name = 'custom_account'

urlpatterns = [
    path('accounts/signup/',
         AccountTypeView.as_view(), name='account_type'),
    path('accounts/signup/tech/',
         TechUserSignupView.as_view(), name='tech_user_signup'),
    path('accounts/signup/recruiter/',
         RecruiterUserSignupView.as_view(), name='recruiter_user_signup'),
    path('user/<slug:slug>/edit/',
         UserProfileEditView.as_view(), name='profile_edit'),
    path('user/<slug:slug>/settings/',
         UserSettingsView.as_view(), name='user_settings'),
    path('user/<slug:slug>/delete/', delete_user, name='delete_user'),
    path('user/<slug:slug>/', UserProfileDetailView.as_view(), name='user_profile'),
]

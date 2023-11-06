"""stackportfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from custom_account.views import (
    TechUserSignupView,
    RecruiterUserSignupView,
    UserProfileDetailView,
    IndexView,
    UserProfileEditView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', IndexView.as_view(), name='homepage'),
    path('accounts/signup/tech/',
         TechUserSignupView.as_view(), name='tech_user_signup'),
    path('accounts/signup/recruiter/',
         RecruiterUserSignupView.as_view(), name='recruiter_user_signup'),
    path('user/<slug:slug>/edit/',
         UserProfileEditView.as_view(), name='profile_edit'),
    path('user/<slug:slug>/', UserProfileDetailView.as_view(), name='user_profile'),

]

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, TechUserProfile, RecruiterUserProfile


class UserProfileTypeFilter(admin.SimpleListFilter):
    title = _('Profile Type')
    parameter_name = 'profile_type'

    def lookups(self, request, model_admin):
        return (
            ('tech', _('Tech User')),
            ('recruiter', _('Recruiter User')),
            ('none', _('None')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'tech':
            return queryset.filter(tech_profile__isnull=False)
        if self.value() == 'recruiter':
            return queryset.filter(recruiter_profile__isnull=False)
        if self.value() == 'none':
            return queryset.filter(tech_profile__isnull=True, recruiter_profile__isnull=True)
        return queryset


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin class for CustomUser.
    Controls the layout and filtering in the Admin.
    """
    list_display = ('email', 'first_name', 'last_name', 'country',
                    'user_profile_type', 'work_title', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', UserProfileTypeFilter)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    actions = ['toggle_active_users', 'toggle_staff_users']

    def user_profile_type(self, obj):
        if hasattr(obj, 'tech_profile') and hasattr(obj, 'recruiter_profile'):
            return "Tech and Recruiter User"
        if hasattr(obj, 'tech_profile'):
            return "Tech User"
        elif hasattr(obj, 'recruiter_profile'):
            return "Recruiter User"
        return "None"

    user_profile_type.short_description = 'Profile Type'

    def toggle_active_users(self, request, queryset):
        """
        Toggle the active status of users.
        """
        for user in queryset:
            user.is_active = not user.is_active
            user.save()

    toggle_active_users.short_description = 'Toggle Active Status'

    def toggle_staff_users(self, request, queryset):
        """
        Toggle the staff status of users.
        """
        for user in queryset:
            user.is_staff = not user.is_staff
            user.save()

    toggle_staff_users.short_description = 'Toggle Staff Status'


@admin.register(TechUserProfile)
class TechUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_first_name', 'user_last_name',
                    'num_projects', 'seeking_employment', 'github_username')
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'github_username')
    list_filter = ('seeking_employment',)

    def user_email(self, obj):
        return obj.user.email

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    def num_projects(self, obj):
        return obj.user.projects.count()

    user_email.short_description = 'Email'
    user_first_name.short_description = 'First Name'
    user_last_name.short_description = 'Last Name'
    num_projects.short_description = 'Number of Projects'


@admin.register(RecruiterUserProfile)
class RecruiterUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_first_name',
                    'user_last_name', 'num_job_posts')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

    def user_email(self, obj):
        return obj.user.email

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    def num_job_posts(self, obj):
        return obj.user.job_posts.count()

    user_email.short_description = 'Email'
    user_first_name.short_description = 'First Name'
    user_last_name.short_description = 'Last Name'
    num_job_posts.short_description = 'Number of Job Posts'

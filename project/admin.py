from django.contrib import admin
from .models import Project, Tech


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_email', 'active', 'github_repo_url',
                    'deployed_url', 'view_count', 'date_created',
                    'date_updated')
    search_fields = ('name', 'user__email', 'description',
                     'github_repo_url', 'deployed_url')
    list_filter = ('active', 'technologies', 'user')
    ordering = ('-date_created', 'name')
    actions = ['toggle_active']

    def user_email(self, obj):
        return obj.user.email

    def view_count(self, obj):
        return obj.num_view_count()

    user_email.short_description = 'User Email'
    view_count.short_description = 'View Count'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('technologies')
        return queryset

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "technologies":
            kwargs["queryset"] = Tech.objects.filter(is_approved=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def toggle_active(self, request, queryset):
        queryset.update(active=not queryset.first().active)

    toggle_active.short_description = 'Toggle Active'

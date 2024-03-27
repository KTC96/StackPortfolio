from django.contrib import admin
from .models import JobPost, Tech, WorkLocationType


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_email', 'company', 'location',
                    'salary_from', 'salary_to', 'salary_currency', 'active',
                    'view_count', 'date_created', 'date_updated')
    search_fields = ('name', 'user__email', 'company', 'location')
    list_filter = ('active', 'company', 'location',
                   'salary_currency', 'technologies', 'work_location_type')
    ordering = ('-date_created', 'name')
    actions = ['toggle_active']

    @admin.display(
        description='Author Email'
    )
    def author_email(self, obj):
        return obj.user.email

    @admin.display(
        description='View Count'
    )
    def view_count(self, obj):
        return obj.num_view_count()


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related(
            'technologies', 'work_location_type')
        return queryset

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "technologies":
            kwargs["queryset"] = Tech.objects.filter(is_approved=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    @admin.action(
        description='Toggle Active'
    )
    def toggle_active(self, request, queryset):
        queryset.update(active=not queryset.first().active)

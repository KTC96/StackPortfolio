from django.contrib import admin
from .models import Tech


@admin.register(Tech)
class TechAdmin(admin.ModelAdmin):
    list_display = ('tech_name', 'is_approved')
    search_fields = ('tech_name',)
    list_filter = ('is_approved',)
    actions = ['approve_tech', 'unapprove_tech',
               'uppercase_tech_name', 'capitalise_tech_name']

    @admin.action(
        description='Approve selected technologies'
    )
    def approve_tech(self, request, queryset):
        queryset.update(is_approved=True)


    @admin.action(
        description='Unapprove selected technologies'
    )
    def unapprove_tech(self, request, queryset):
        queryset.update(is_approved=False)


    @admin.action(
        description='Uppercase tech names of selected technologies'
    )
    def uppercase_tech_name(self, request, queryset):
        for tech in queryset:
            tech.tech_name = tech.tech_name.upper()
            tech.save()


    @admin.action(
        description='Capitalise tech names of selected technologies'
    )
    def capitalise_tech_name(self, request, queryset):
        for tech in queryset:
            tech.tech_name = tech.tech_name.capitalize()
            tech.save()


from django.contrib import admin
from .models import Tech


@admin.register(Tech)
class TechAdmin(admin.ModelAdmin):
    list_display = ('tech_name', 'is_approved')
    search_fields = ('tech_name',)
    list_filter = ('is_approved',)
    actions = ['approve_tech', 'unapprove_tech',
               'uppercase_tech_name', 'capitalise_tech_name']

    def approve_tech(self, request, queryset):
        queryset.update(is_approved=True)

    approve_tech.short_description = 'Approve selected technologies'

    def unapprove_tech(self, request, queryset):
        queryset.update(is_approved=False)

    unapprove_tech.short_description = 'Unapprove selected technologies'

    def uppercase_tech_name(self, request, queryset):
        for tech in queryset:
            tech.tech_name = tech.tech_name.upper()
            tech.save()

    uppercase_tech_name.short_description = (
        'Uppercase tech names of selected technologies'
    )

    def capitalise_tech_name(self, request, queryset):
        for tech in queryset:
            tech.tech_name = tech.tech_name.capitalize()
            tech.save()

    capitalise_tech_name.short_description = (
        'Capitalise tech names of selected technologies'
    )

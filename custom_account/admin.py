from django.contrib import admin
from .models import CustomUser, TechUserProfile, RecruiterUserProfile

admin.site.register(CustomUser)
admin.site.register(TechUserProfile)
admin.site.register(RecruiterUserProfile)

from django.urls import path
from .views import JobPostDetailView

app_name = 'job_post'

urlpatterns = [
    path('<slug:slug>/job/<int:id>/',
         JobPostDetailView.as_view(), name='view_job_post'),
]

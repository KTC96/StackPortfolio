from django.urls import path
from .views import JobPostDetailView, JobPostCreateView

app_name = 'job_post'

urlpatterns = [
    path('<slug:slug>/job/<int:id>/',
         JobPostDetailView.as_view(), name='view_job_post'),
    path('<slug:slug>/job/create', JobPostCreateView.as_view(),
         name='create_job_post'),
]

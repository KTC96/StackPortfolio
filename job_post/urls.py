from django.urls import path
from .views import (JobPostDetailView,
                    JobPostCreateView,
                    JobPostEditView,
                    delete_job_post
                    )

app_name = 'job_post'

urlpatterns = [
    path('<slug:slug>/job/create', JobPostCreateView.as_view(),
         name='create_job_post'),
    path('<slug:slug>/job/<int:id>/edit', JobPostEditView.as_view(),
         name='edit_job_post'),
    path('<slug:slug>/job/<int:id>/delete/', delete_job_post,
         name='delete_job_post'),
    path('<slug:slug>/job/<int:id>/',
         JobPostDetailView.as_view(), name='view_job_post'),

]

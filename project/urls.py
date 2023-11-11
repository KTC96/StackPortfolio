from django.urls import path
from .views import ProjectDetailView

app_name = 'project'

urlpatterns = [
    path('<slug:slug>/project/<slug:project_slug>',
         ProjectDetailView.as_view(), name='view_project'),
]

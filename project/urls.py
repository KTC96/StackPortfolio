from django.urls import path
from .views import ProjectDetailView, ProjectCreateView, ProjectEditView, delete_project

app_name = 'project'

urlpatterns = [
    path('<slug:slug>/project/create',
         ProjectCreateView.as_view(), name='create_project'),
    path('<slug:slug>/project/<slug:project_slug>/edit',
         ProjectEditView.as_view(), name='edit_project'),
    path('<slug:slug>/project/<slug:project_slug>/delete/',
         delete_project, name='delete_project'),
    path('<slug:slug>/project/<slug:project_slug>',
         ProjectDetailView.as_view(), name='view_project'),

]

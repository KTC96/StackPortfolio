from django.urls import path
from .views import ProjectDetailView, ProjectCreateView

app_name = 'project'

urlpatterns = [
    path('<slug:slug>/project/create',
         ProjectCreateView.as_view(), name='create_project'),
    path('<slug:slug>/project/<slug:project_slug>',
         ProjectDetailView.as_view(), name='view_project'),

]

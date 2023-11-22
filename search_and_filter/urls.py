from django.urls import path
from .views import SearchResultsView


app_name = 'search_and_filter'

urlpatterns = [
    path('', SearchResultsView.as_view(), name='search_results'),
]

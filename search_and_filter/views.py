from django.shortcuts import render
from django.views.generic import ListView
from project.models import Project
from django.db.models import Q


class SearchResultsView(ListView):
    """
    Handles the display of search results.
    """
    template_name = 'search_results_page.html'
    model = Project

    def get_queryset(self):
        """
        Returns the queryset of projects that match the search term.
        """
        query = self.request.GET.get('q', '')

        if query:
            object_list = Project.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            object_list = Project.objects.all()

        return object_list

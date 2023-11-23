from django.views.generic import ListView
from project.models import Project
from job_post.models import JobPost
from custom_account.models import CustomUser
from django.db.models import Q


class SearchResultsView(ListView):
    """
    Handles the display of search results.
    """
    template_name = 'search_results_page.html'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', 'users')

        if search_type == 'projects':
            return Project.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        elif search_type == 'job_posts':
            return JobPost.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            return CustomUser.objects.filter(
                Q(first_name__icontains=query) | Q(
                    last_name__icontains=query) | Q(bio__icontains=query)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_type = self.request.GET.get('type', 'users')
        context['search_type'] = search_type
        context['current_query'] = self.request.GET.get('q', '')
        return context

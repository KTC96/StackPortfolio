from django.views.generic import ListView
from project.models import Project
from job_post.models import JobPost
from technology.models import Tech
from custom_account.models import CustomUser
from django.db.models import Q


class SearchResultsView(ListView):
    """
    Handles the display of search results.
    """
    template_name = 'search_results_page.html'
    paginate_by = 9

    def filter_by_technologies(self, queryset, tech_names, match_type, model):
        if not tech_names:
            return queryset

        if model == CustomUser:
            tech_qs = Tech.objects.filter(tech_name__in=tech_names)
            if match_type == 'all':
                for tech in tech_qs:
                    queryset = queryset.filter(tech_profile__technologies=tech)
            elif match_type == 'any':
                queryset = queryset.filter(
                    tech_profile__technologies__in=tech_qs)
            return queryset.distinct()

        tech_qs = Tech.objects.filter(tech_name__in=tech_names)
        if match_type == 'all':
            for tech in tech_qs:
                queryset = queryset.filter(technologies=tech)
        elif match_type == 'any':
            queryset = queryset.filter(technologies__in=tech_qs)
        return queryset.distinct()

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', 'users')
        tech_match_type = self.request.GET.get('tech_match_type', 'all')
        selected_tech_names = self.request.GET.get('selectedTechnologies')
        if selected_tech_names:
            selected_tech_names = selected_tech_names.split(',')
        else:
            selected_tech_names = []

        if search_type == 'projects':
            queryset = Project.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).filter(active=True)
        elif search_type == 'job_posts':
            queryset = JobPost.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).filter(active=True)
        else:
            queryset = CustomUser.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) |
                Q(email__icontains=query) | Q(bio__icontains=query)
            ).filter(is_active=True)

        return self.filter_by_technologies(
            queryset,
            selected_tech_names,
            tech_match_type,
            CustomUser if search_type == 'users' else Project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_type = self.request.GET.get('type', 'users')
        context['search_type'] = search_type
        context['current_query'] = self.request.GET.get('q', '')
        context['approved_technologies'] = Tech.objects.filter(
            is_approved=True).order_by('tech_name')
        selected_tech_names = self.request.GET.get(
            'selectedTechnologies', '').split(',')
        context['selected_technologies'] = Tech.objects.filter(
            tech_name__in=selected_tech_names, is_approved=True)
        context['tech_match_type'] = self.request.GET.get(
            'tech_match_type', 'any')
        return context

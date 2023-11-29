from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, CreateView, UpdateView
import cloudinary.uploader
import cloudinary
from .models import Project
from .forms import ProjectForm
from technology.models import Tech


class ProjectDetailView(DetailView):
    """
    This view handles the displaying of a
    single project on its own page.
    """
    model = Project
    template_name = 'project_page.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self):
        """
        Returns the project object based on the project_slug and user slug.
        """
        project_slug = self.kwargs['project_slug']
        user_slug = self.kwargs.get('slug')
        return get_object_or_404(
            Project,
            slug=project_slug,
            user__slug=user_slug)

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)
        return context


class ProjectListView(ListView):
    """
    This view lists all the projects on the
    a project list page.
    """
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        """
        Returns all the projects.
        """
        return Project.objects.filter(
            active=True).order_by('-date_created')


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    Class to handle project creation.
    """
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.slug == self.kwargs['slug']):
            messages.error(
                request, "You are not authorised to view this page.")
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_technologies'] = Tech.objects.all().filter(
            is_approved=True)
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user
        project.save()

        # Add existing technologies
        existing_tech_ids = form.cleaned_data.get('technologies')
        for tech_id in existing_tech_ids:
            project.technologies.add(tech_id)

        # If a tech is submitting and it's not
        # in the database, add it to the database
        # as unapproved.
        new_tech_names = self.request.POST.get(
            'new_technologies', '').split(',')
        for tech_name in new_tech_names:
            tech_name = tech_name.strip()
            if tech_name:
                tech, created = Tech.objects.get_or_create(
                    tech_name=tech_name, defaults={'is_approved': False})
                project.technologies.add(tech)

        messages.success(
            self.request, "New project successfully added.")

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, "Project creation failed. Please check your inputs.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            'custom_account:user_profile', kwargs={
                'slug': self.request.user.slug})


class ProjectEditView(LoginRequiredMixin, UpdateView):
    """
    This class handles making updates to the project.
    """
    model = Project
    form_class = ProjectForm
    template_name = 'edit_project.html'
    slug_field = 'slug'
    slug_url_kwarg = 'project_slug'

    def get_object(self):
        project_slug = self.kwargs['project_slug']
        user_slug = self.kwargs['slug']
        return get_object_or_404(
            Project,
            slug=project_slug,
            user__slug=user_slug)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and
                request.user.slug == self.kwargs['slug']):
            messages.error(
                request, "You are not authorized to view this page.")
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_technologies'] = Tech.objects.all().filter(
            is_approved=True)
        context['project_technologies'] = self.object.technologies.all()

        return context

    def remove_tech_from_project(self, project, tech_id):
        """
        Remove a tech from a project.
        """
        project.technologies.remove(tech_id)

        # If the tech is not associated with any other projects,
        # delete it from the database.
        if not Tech.objects.filter(projects__technologies=tech_id).exists():
            Tech.objects.filter(id=tech_id).delete()

    def form_valid(self, form):
        # Get the current project instance from the database
        current_project = Project.objects.get(pk=self.object.pk)

        # Get the old image public ID before it gets updated
        old_image_public_id = None
        if 'image' in form.changed_data:
            old_image_public_id = current_project.image.public_id

        project = form.save(commit=False)
        project.user = self.request.user
        project.save()

        project.technologies.clear()

        existing_tech_ids = form.cleaned_data.get('technologies', [])
        for tech_id in existing_tech_ids:
            project.technologies.add(tech_id)

        # If a tech is submitted and it's not
        # in the database, add it to the database
        # as unapproved.
        new_tech_names = self.request.POST.get(
            'new_technologies', '').split(',')
        for tech_name in new_tech_names:
            tech_name = tech_name.strip()
            if tech_name:
                tech, created = Tech.objects.get_or_create(
                    tech_name=tech_name, defaults={'is_approved': False})
                project.technologies.add(tech)

        # if project image has changed, delete the old image
        if old_image_public_id:
            try:
                cloudinary.uploader.destroy(
                    old_image_public_id, invalidate=True)
            except Exception as e:
                print(e)
                messages.error(
                    self.request,
                    "There was an error deleting the old image.")

        messages.success(
            self.request, "Project successfully updated.")

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, "Project update failed. Please check your inputs.")
        return super().form_invalid(form)


@login_required
@require_POST
def delete_project(request, slug, project_slug):
    """
    Handles project deletion.
    """
    user = request.user
    project = get_object_or_404(Project, slug=project_slug, user__slug=slug)

    if user == project.user:

        if project.image:
            # Get the previous image id before deleting the project
            image_public_id = project.image.public_id

        project.delete()

        if project.image:
            try:
                cloudinary.uploader.destroy(image_public_id, invalidate=True)
                messages.success(
                    request, "Project image has been successfully deleted.")
            except Exception as e:
                print(e)
                messages.warning(
                    request,
                    "Project deleted, but there was an error deleting\n",
                    "the image from Cloudinary. Please check manually.")

        messages.success(
            request, "Your project has been successfully deleted.")
        return redirect(
            reverse(
                'custom_account:user_profile',
                kwargs={
                    'slug': slug}))

    messages.error(
        request, "You cannot delete this project.")
    return redirect(
        reverse(
            'custom_account:user_profile',
            kwargs={
                'slug': slug}))

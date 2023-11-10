from django.test import TestCase
from django.apps import apps
from custom_account.models import CustomUser
from project.models import Project


class ProjectCreationTests(TestCase):
    """
    Tests for project creation.
    """

    def setUp(self):
        """Create a user to associate with the project."""
        self.user = CustomUser.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='password',
        )

    def test_check_model_is_not_none(self):
        """Test case to check if model is not none"""
        try:
            apps.get_model('project', 'Project')
        except LookupError as e:
            self.fail(f"Failed to get Project model. Error: {e}")

    def test_create_project(self):
        """Test to create a project."""
        try:
            # Create a project with dummy data
            project = Project.objects.create(
                project_name='Test Project',
                user=self.user,
                github_repo_url=''
            )
        except Exception as e:
            self.fail(f"Failed to create project. Error: {e}")

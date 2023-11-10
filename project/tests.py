from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
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

    def test_project_without_project_name(self):
        """Test to prevent project creation without a project name."""
        project = Project.objects.create(
            project_name='',
            user=self.user,
            github_repo_url=''
        )

        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_project_without_user(self):
        """Test to prevent project creation without a user."""
        with self.assertRaises(IntegrityError):
            Project.objects.create(
                project_name='Test Project',
                user=None,
                github_repo_url=''
            )

    def test_project_name_fewer_than_100_characters(self):
        """Test to prevent project creation with a project name longer than 100 characters."""
        project = Project.objects.create(
            project_name='a' * 101,
            user=self.user,
            github_repo_url=''
        )

        with self.assertRaises(ValidationError):
            project.full_clean()

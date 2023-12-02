from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from custom_account.models import CustomUser, RecruiterUserProfile
from job_post.models import JobPost
from work_location_type.models import WorkLocationType


class JobPostCreationTests(TestCase):
    """
    Tests for job post creation.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='recruiteruser',
            first_name='Recruiter',
            last_name='User',
            email='recruiteruser@example.com',
            password='password',
        )
        RecruiterUserProfile.objects.create(user=self.user)

        self.user2 = CustomUser.objects.create_user(
            username='anotheruser',
            first_name='Another',
            last_name='User',
            email='anotheruser@example.com',
            password='password',
        )

    def test_job_post_creation(self):
        """
        Test that a job post can be created.
        """
        job_post = JobPost.objects.create(
            user=self.user,
            name='Test Job Post',
            description='This is a test job post.',
            location='Test Location',
            salary_from='10000',
            salary_to='20000',
        )
        self.assertEqual(job_post.user, self.user)
        self.assertEqual(job_post.name, 'Test Job Post')
        self.assertEqual(job_post.description, 'This is a test job post.')
        self.assertEqual(job_post.location, 'Test Location')
        self.assertEqual(job_post.salary_from, '10000')
        self.assertEqual(job_post.salary_to, '20000')
        self.assertEqual(job_post.active, True)

    def test_job_post_creation_with_no_user(self):
        """
        Test that a job post cannot be created without a user.
        """
        with self.assertRaises(IntegrityError):
            JobPost.objects.create(
                user=None,
                name='Test Job Post',
                description='This is a test job post.',
                location='Test Location',
                salary_from='10000',
                salary_to='20000',
            )

    def test_job_post_without_recruiter_user_profile(self):
        """
        Test to prevent job post creation without a recruiter user profile.
        """
        with self.assertRaises(IntegrityError):
            JobPost.objects.create(
                name='Test Job Post',
                user=self.user2,
            )

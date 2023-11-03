from django.db import IntegrityError
from django.test import TestCase
from django.apps import apps
from custom_account.models import ParentUser


class AccountTests(TestCase):
    """
    Tests for creating, updating, and deleting
    users in the custom_account app.
    """

    def test_check_create_user_view_exists(self):
        """Test case to check if model is not none"""
        try:
            UserModel = apps.get_model('custom_account', 'ParentUser')
        except LookupError as e:
            self.fail(f"Failed to get User model. Error: {e}")

    def test_create_and_retrieve_user(self):
        """Test to create and get back a user from the database."""

        try:
            # Create a user with dummy data
            user = ParentUser.objects.create(
                email='test@test.com',
                username='testuser',
                first_name='Test',
                last_name='User',
                password='testpassword123',
            )
        except IntegrityError as e:
            self.fail(f"Failed to create user. Error: {e}")

        try:
            # Pull the user from the database if it exists
            existing_user = ParentUser.objects.get(pk=user.pk)
        except ParentUser.DoesNotExist as e:  # pylint: disable=no-member
            self.fail(f"Could not get user from the database. Error: {e}")

        # Check the data matches what was created
        self.assertEqual(existing_user.email, 'test@test.com')
        self.assertEqual(existing_user.username, 'testuser')
        self.assertEqual(existing_user.first_name, 'Test')
        self.assertEqual(existing_user.last_name, 'User')

    def test_additional_user_fields_exist(self):
        """
        Test to see if the fields added to the
        custom user model exist.
        """
        try:
            # Create a user with dummy data
            user = ParentUser.objects.create(
                email='test@test.com',
                username='testuser',
                first_name='Test',
                last_name='User',
                password='testpassword123',
                town_city='test town',
                display_town_city=True,
                country='test country',
                display_email=False,
                website='',
                phone_number='123456789',
                display_phone_number=False,
                profile_image='testprofileimageurl.com',
                bio='test bio',
                work_title='test work title',
                company='test company',
                linkedin_username='testuser22',
                twitter_handle='testuser22',
            )
        except IntegrityError as e:
            self.fail(f"Failed to create user with all fields. Error: {e}")

        try:
            # Pull the user from the database if it exists
            existing_user = ParentUser.objects.get(pk=user.pk)
        except ParentUser.DoesNotExist as e:  # pylint: disable=no-member
            self.fail(f"Could not get user from the database. Error: {e}")

        # Check the data matches what was created
        self.assertEqual(existing_user.town_city, 'test town')
        self.assertEqual(existing_user.display_town_city, True)
        self.assertEqual(existing_user.country, 'test country')
        self.assertEqual(existing_user.display_email, False)
        self.assertEqual(existing_user.website, '')
        self.assertEqual(existing_user.phone_number, '123456789')
        self.assertEqual(existing_user.display_phone_number, False)
        self.assertEqual(existing_user.profile_image,
                         'testprofileimageurl.com')
        self.assertEqual(existing_user.bio, 'test bio')
        self.assertEqual(existing_user.work_title, 'test work title')
        self.assertEqual(existing_user.company, 'test company')
        self.assertEqual(existing_user.linkedin_username, 'testuser22')
        self.assertEqual(existing_user.twitter_handle, 'testuser22')

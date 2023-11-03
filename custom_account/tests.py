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
        except Exception as e:
            self.fail(f"Failed to create user. Error: {e}")

        try:
            # Pull the user from the database if it exists
            existing_user = ParentUser.objects.get(pk=user.pk)
            
            # Check the the data matches what was created
            self.assertEqual(existing_user.email, 'test@test.com')
            self.assertEqual(existing_user.username, 'testuser')
            self.assertEqual(existing_user.first_name, 'Test')
            self.assertEqual(existing_user.last_name, 'User')
        except Exception as e:
            self.fail(f"Could not get user from the database. Error: {e}")



        

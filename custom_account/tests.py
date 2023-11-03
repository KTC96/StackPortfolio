from django.test import TestCase
from django.apps import apps


class AccountTests(TestCase):
    """
    Test case to check if model is not none
    """
    def test_check_create_user_view_exists(self):
      try:
          UserModel = apps.get_model('account', 'User') 
      except LookupError as e:
          self.fail(f"Failed to get User model. Error: {e}")


        

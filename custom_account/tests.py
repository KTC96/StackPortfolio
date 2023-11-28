"""
Account app tests.
"""
from django.db import IntegrityError
from django.test import TestCase
from django.apps import apps
from custom_account.models import CustomUser


class AccountTests(TestCase):
    """
    Tests for creating, updating, and deleting
    users in the custom_account app.
    """

    def test_check_create_user_view_exists(self):
        """Test case to check if model is not none"""
        try:
            apps.get_model('custom_account', 'CustomUser')
        except LookupError as e:
            self.fail(f"Failed to get User model. Error: {e}")

    def test_create_and_retrieve_user(self):
        """Test to create and get back a user from the database."""

        try:
            # Create a user with dummy data
            user = CustomUser.objects.create(
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
            existing_user = CustomUser.objects.get(pk=user.pk)
        except CustomUser.DoesNotExist as e:  # pylint: disable=no-member
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
            user = CustomUser.objects.create(
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
            existing_user = CustomUser.objects.get(pk=user.pk)
        except CustomUser.DoesNotExist as e:  # pylint: disable=no-member
            self.fail(f"Could not get user from the database. Error: {e}")

        # Check the data matches what was created
        self.assertEqual(existing_user.town_city, 'test town')
        self.assertEqual(existing_user.display_town_city, True)
        self.assertEqual(existing_user.country, 'test country')
        self.assertEqual(existing_user.display_email, False)
        self.assertEqual(existing_user.website, '')
        self.assertEqual(existing_user.phone_number, '123456789')
        self.assertEqual(existing_user.display_phone_number, False)
        self.assertEqual(existing_user.bio, 'test bio')
        self.assertEqual(existing_user.work_title, 'test work title')
        self.assertEqual(existing_user.company, 'test company')
        self.assertEqual(existing_user.linkedin_username, 'testuser22')
        self.assertEqual(existing_user.twitter_handle, 'testuser22')

    def test_create_user_with_empty_email(self):
        """
        Test to ensure a user cannot be created
        with an invalid email address.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='',
                username='testuser',
                first_name='Test',
                last_name='User',
                password='testpassword123',
            )

    def test_create_user_with_invalid_email(self):
        """
        Test to ensure a user cannot be created
        with an invalid email address.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='test@test',
                username='testuser',
                first_name='Test',
                last_name='User',
                password='testpassword123',
            )

    def test_email_already_exists(self):
        """
        Test to ensure a user cannot be created
        with an email address that already exists.
        """
        user = CustomUser.objects.create_user(
            email='user1@test.com',
            username='user1',
            first_name='Test1',
            last_name='User1',
            password='testpassword123'
        )

        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email='user1@test.com',
                username='user2',
                first_name='Test1',
                last_name='User1',
                password='testpassword123'
            )

    def test_create_user_with_empty_username(self):
        """
        Test to ensure a user cannot be created
        with an invalid username.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='test@test.com',
                username='',
                first_name='Test',
                last_name='User',
                password='testpassword123',
            )

    def test_create_user_with_short_username(self):
        """
        Test to ensure a user cannot be created
        with an invalid username.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='test@test.com',
                username='hi',
                first_name='Test',
                last_name='User',
                password='testpassword123',
            )

    def test_create_user_with_long_username(self):
        """
        Test to ensure a user cannot be created
        with an invalid username.
        """
        forty_one_char_username = 'a' * 41
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='test@test.com',
                username=forty_one_char_username,
                first_name='Test',
                last_name='User',
                password='testpassword123',
            )

    def test_create_user_with_symbols_in_username(self):
        """
        Test to ensure a user cannot be created
        with an invalid username.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email='test@test.com',
                username="testuser123!",
                first_name='Test',
                last_name='User',
                password='testpassword123',
            )

    def test_create_user_with_empty_first_name(self):
        """
        Test to ensure a user cannot be created
        with an invalid first name.
        """
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                email='test@test.com',
                username="testuser",
                first_name='',
                last_name='User',
                password='testpassword123'
            )

    def test_create_user_with_short_first_name(self):
        """
        Test to ensure a user cannot be created
        with an invalid first name.
        """
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                email='test@test.com',
                username="testuser",
                first_name='A',
                last_name='User',
                password='testpassword123'
            )

    def test_create_user_with_long_first_name(self):
        """
        Test to ensure a user cannot be created
        with an invalid first name.
        """
        forty_one_char_first_name = 'a' * 41
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                email='test@test.com',
                username="testuser",
                first_name=forty_one_char_first_name,
                last_name='User',
                password='testpassword123'
            )


class AccountUpdateTests(TestCase):
    """
    Tests for updating users in the custom_account app.
    """

    def setUp(self):
        """
        Initial setup for the tests, creating a user to update.
        """
        self.user = CustomUser.objects.create(
            email='update_test@test.com',
            username='updatetestuser',
            first_name='UpdateTest',
            last_name='User',
            password='testpassword123',
            town_city='Update City',
            country='Update Country',
            phone_number='987654321',
            bio='update bio',
            work_title='update work title',
            company='update company',
            linkedin_username='updateuser22',
            twitter_handle='updateuser22',
        )

    def test_update_user_email(self):
        """
        Test to update a user's email address.
        """
        # Change the email of the existing user
        self.user.email = 'updated_email@test.com'
        self.user.save()

        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.email, 'updated_email@test.com')

    def test_update_user_phone_number(self):
        """
        Test to update a user's phone number.
        """
        # Change the phone number of the existing user
        self.user.phone_number = '123456789'
        self.user.save()

        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.phone_number, '123456789')

    def test_toggle_user_email_display(self):
        """
        Test to toggle the user's preference for displaying their email.
        """
        original_display_email = self.user.display_email
        self.user.display_email = not self.user.display_email
        self.user.save()

        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.display_email,
                         not original_display_email)

    def test_update_multiple_fields(self):
        """
        Test to update multiple fields of a user at once.
        """
        # Update multiple fields of the user
        self.user.bio = 'New updated bio'
        self.user.work_title = 'New updated title'
        self.user.company = 'New updated company'
        self.user.save()

        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.bio, 'New updated bio')
        self.assertEqual(updated_user.work_title, 'New updated title')
        self.assertEqual(updated_user.company, 'New updated company')


class AccountDeleteTests(TestCase):
    """
    Tests for deleting users in the custom_account app.
    """

    def setUp(self):
        """
        Initial setup for the tests, creating a user to delete.
        """
        self.user = CustomUser.objects.create(
            email='delete_test@test.com',
            username='deletetestuser',
            first_name='DeleteTest',
            last_name='User',
            password='testpassword123',
            town_city='Delete City',
            country='Delete Country',
            phone_number='123456789',
            bio='delete bio',
            work_title='delete work title',
            company='delete company',
            linkedin_username='deleteuser22',
            twitter_handle='deleteuser22',
        )

    def test_user_deletion(self):
        """
        Test to ensure a user is correctly deleted.
        """
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(CustomUser.DoesNotExist):  # pylint: disable=no-member
            CustomUser.objects.get(id=user_id)

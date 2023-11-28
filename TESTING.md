# Testing

## Overview

I am using a combination of automated and manual testing in my project.

## Automated Testing

### Account

In my Account tests, I test for the creation, updating and deletion of accounts.

#### Create Account

Unittest

1. Test that the User model is not none with `test_check_create_user_view_exists`.
2. Test for creating and retrieving a user from the database with `test_create_and_retrieve_user`.
3. Test that additional user fields exist with `test_additional_user_fields_exist`.
4. Test that the user cannot sign up with an email with `test_create_user_with_empty_email`.
5. Test that the user cannot sign up with an invalid email with `test_create_user_with_invalid_email`.
6. Test that the user cannot sign up with an email that already exists with `test_email_already_exists`.
7. Test that the user cannot sign up with an empty username with `test_create_user_with_empty_username`.
8. Test that the user cannot sign up with a username with fewer than 2 characters with `test_create_user_with_short_username`.
9. Test that the user cannot sign up with a username with more than 20 characters with `test_create_user_with_long_username`.
10. Test that the user cannot sign up with a username with symbols with `test_create_user_with_symbols_in_username`.
11. Test that the user cannot sign up with an empty first name with `test_create_user_with_empty_first_name`.
12. Test that the user cannot sign up with a first name with fewer than 2 characters with `test_create_user_with_short_first_name`.
13. Test that the user cannot sign up with a first name with more than 20 characters with `test_create_user_with_long_first_name`.

Jest

1. Test that the validate input function exists with `function exists`.
2. Check that an empty input is invalid with `shows error if input is empty, touched and required`.
3. Check that an input cannot be filled with blank spaces with `shows error if input is multiple spaces`.
4. Check that a text input cannot have fewer than 2 characters with `shows error if input is less than 2 characters`.

#### Update Account

1. Test that the email gets updated with `test_update_user_email`.
2. Test that the phone number gets updated with `test_update_user_phone_number`.
3. Test that the email display gets toggled with `test_toggle_user_email_display`.
4. Test that multiple fields get updated with `test_update_multiple_fields`.

#### Delete Account

1. Test that the user gets deleted with `test_delete_user` - this test requires that the `self.user.delete()` line in the test is commented out for the test to fail.

### Project

#### Create Project

Unittest

1. Test that the Project model is not none with `test_check_model_is_not_none`.
2. Test that a project can be created with `test_create_project`.
3. Test that a project cannot be created without a project name with `test_project_without_project_name`.
4. Test that a project cannot be created without a user with `test_project_without_user`.
5. Test that a project cannot be created with a project name with more than 100 characters with `test_project_name_fewer_than_100_characters`.

#### Project Detail

1. Test that the Project Detail view exists with `test_project_detail_view_exists`.

#### Project List

1. Test that the Project List view exists with `test_project_list_view_exists`.

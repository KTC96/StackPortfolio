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

Jest

1. Test that the validate input function exists with `function exists`.
2. Check that an empty input is invalid with `returns false if input is empty`.
3. Check that an input cannot be filled with blank spaces with `returns false if input multiple spaces`.
4. Check that a text input cannot have fewer than 2 characters with `returns false if input is less than 2 characters`.
5. Check that first_name and last_name cannot have more than 40 characters with `returns false if first_name or last_name is more than 41 characters`.

#### Update Account

1. Test that the email gets updated with `test_update_user_email`.
2. Test that the phone number gets updated with `test_update_user_phone_number`.
3. Test that the email display gets toggled with `test_toggle_user_email_display`.
4. Test that multiple fields get updated with `test_update_multiple_fields`.

#### Delete Account

1. Test that the user gets deleted with `test_delete_user` - this test requires that the `self.user.delete()` line in the test is commented out for the test to fail.

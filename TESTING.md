# Testing

## Overview

I am using a combination of automated and manual testing in my project.

## Automated Testing

### Account

In my Account tests, I test for the creation, updating and deletion of accounts.

#### Create Account

1. Test that the User model is not none with `test_check_create_user_view_exists`.
2. Test for creating and retrieving a user from the database with `test_create_and_retrieve_user`.
3. Test that additional user fields exist with `test_additional_user_fields_exist`.

#### Update Account

1. Test that the email gets updated with `test_update_user_email`.
2. Test that the phone number gets updated with `test_update_user_phone_number`.
3. Test that the email display gets toggled with `test_toggle_user_email_display`.
4. Test that multiple fields get updated with `test_update_multiple_fields`.

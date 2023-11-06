# Testing

## Overview

I am using a combination of automated and manual testing in my project.

## Automated Testing

### Account

In my Account tests, I test for the creation, updating and deletion of accounts:

1. Test that the User model is not none with `test_check_create_user_view_exists`.
2. Test for creating and retrieving a user from the database with `test_create_and_retrieve_user`.
3. Test that additional user fields exist with `test_additional_user_fields_exist`.

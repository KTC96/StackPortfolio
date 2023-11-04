# Testing

## Overview

I am using a combination of automated and manual testing in my project.

## Automated Testing

### Account

In my Account tests, I test for the creation, updating and deletion of accounts:

1. Test that the User model is not none with `test_check_create_user_view_exists`.
2. Test for creating and retrieving a user from the database with `test_create_and_retrieve_user`.
3. Test that additional user fields exist with `test_additional_user_fields_exist`.
4. Test to see that a TechUser can be created using the fields from the ParentUser using `test_tech_user_creation`.
5. Test that the TechUser can have the inherited fields, but also its own additional fields with `test_tech_user_additional_fields`.
6. Test to see that a RecruiterUser can be created using the fields from the ParentUser using `test_recruiter_user_creation`

# Testing

## Overview

I am using a combination of automated and manual testing in my project.

## Automated Testing

### Account

#### Create Account

##### Create Account Unittest

| Test Name                                   | Description                                                         | Status |
| ------------------------------------------- | ------------------------------------------------------------------- | ------ |
| `test_check_create_user_view_exists`        | Test that the User model is not none                                | Pass   |
| `test_create_and_retrieve_user`             | Test for creating and retrieving a user                             | Pass   |
| `test_additional_user_fields_exist`         | Test that additional user fields exist                              | Pass   |
| `test_create_user_with_empty_email`         | Test that the user cannot sign up with an empty email               | Pass   |
| `test_create_user_with_invalid_email`       | Test that the user cannot sign up with an invalid email             | Pass   |
| `test_email_already_exists`                 | Test that the user cannot sign up with an email that already exists | Pass   |
| `test_create_user_with_empty_username`      | Test that the user cannot sign up with an empty username            | Pass   |
| `test_create_user_with_short_username`      | Test that the user cannot sign up with a short username             | Pass   |
| `test_create_user_with_long_username`       | Test that the user cannot sign up with a long username              | Pass   |
| `test_create_user_with_symbols_in_username` | Test that the user cannot sign up with symbols in the username      | Pass   |
| `test_create_user_with_empty_first_name`    | Test that the user cannot sign up with an empty first name          | Pass   |
| `test_create_user_with_short_first_name`    | Test that the user cannot sign up with a short first name           | Pass   |
| `test_create_user_with_long_first_name`     | Test that the user cannot sign up with a long first name            | Pass   |

##### Create Account Jest

| Test Name                                             | Description                                                 | Status |
| ----------------------------------------------------- | ----------------------------------------------------------- | ------ |
| `function exists`                                     | Test that the validate input function exists                | Pass   |
| `shows error if input is empty, touched and required` | Check that an empty input is invalid                        | Pass   |
| `shows error if input is multiple spaces`             | Check that an input cannot be filled with blank spaces      | Pass   |
| `shows error if input is less than 2 characters`      | Check that a text input cannot have fewer than 2 characters | Pass   |

#### Update Account

##### Update Account Unittest

| Test Name                        | Description                              | Status |
| -------------------------------- | ---------------------------------------- | ------ |
| `test_update_user_email`         | Test that the email gets updated         | Pass   |
| `test_update_user_phone_number`  | Test that the phone number gets updated  | Pass   |
| `test_toggle_user_email_display` | Test that the email display gets toggled | Pass   |
| `test_update_multiple_fields`    | Test that multiple fields get updated    | Pass   |

#### Delete Account

##### Delete Account Unittest

| Test Name          | Description                     | Status |
| ------------------ | ------------------------------- | ------ |
| `test_delete_user` | Test that the user gets deleted | Pass   |

---

### Project

#### Create Project

##### Project Unittest

| Test Name                                     | Description                                                       | Status |
| --------------------------------------------- | ----------------------------------------------------------------- | ------ |
| `test_check_model_is_not_none`                | Test that the Project model is not none                           | Pass   |
| `test_create_project`                         | Test that a project can be created                                | Pass   |
| `test_project_without_project_name`           | Test that a project cannot be created without a project name      | Pass   |
| `test_project_without_user`                   | Test that a project cannot be created without a user              | Pass   |
| `test_project_name_fewer_than_100_characters` | Test that a project cannot be created with a long project name    | Pass   |
| `test_project_without_tech_user_profile`      | Test that a project cannot be created without a tech user profile | Pass   |
| `test_unique_project_name`                    | Test that a user's project has a unique name                      | Pass   |

#### Update Project

##### Update Project Unittest

| Test Name                                | Description                                                   | Status |
| ---------------------------------------- | ------------------------------------------------------------- | ------ |
| `test_project_update`                    | Test that a project can be updated                            | Pass   |
| `test_update_project_with_existing_name` | Test that a project cannot be updated with an existing name   | Pass   |
| `test_update_project_with_invalid_url`   | Test that a project cannot be updated with an invalid URL     | Pass   |
| `test_update_project_description_length` | Test that a project cannot be updated with a long description | Pass   |
| `test_update_project_without_changes`    | Test that a project cannot be updated without changes         | Pass   |

#### Project Detail

##### Project Detail Unittest

| Test Name                         | Description                              | Status |
| --------------------------------- | ---------------------------------------- | ------ |
| `test_project_detail_view_exists` | Test that the Project Detail view exists | Pass   |

#### Project List

##### Project List Unittest

| Test Name                       | Description                            | Status |
| ------------------------------- | -------------------------------------- | ------ |
| `test_project_list_view_exists` | Test that the Project List view exists | Pass   |

---

### Job Post

#### Create Job Post

##### Create Job Post Unittest

| Test Name                                      | Description                                                        | Status |
| ---------------------------------------------- | ------------------------------------------------------------------ | ------ |
| `test_job_post_creation`                       | Test that a job can be created                                     | Pass   |
| `test_job_post_creation_with_no_user`          | Test that a job cannot be created without a user                   | Pass   |
| `test_job_post_without_recruiter_user_profile` | Test that a job cannot be created without a recruiter user profile | Pass   |

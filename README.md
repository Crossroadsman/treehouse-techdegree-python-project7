Project 7: User Profile With Django
===================================

Note: The minimum version of Python compatible with this project is 3.6 (December 2016)

Superuser
---------

- User: test@test.com
- Password: Project7-UserProfile

Feature Checklist
-----------------

### Base Features ###

- [x]: Uses provided base HTML/CSS
- [ ]: Has Django model for user profile
- [ ]: Has routes to:
  - [ ]: Display a profile
  - [ ]: Edit a profile
  - [ ]: Change the password
- [ ]: Has a "profile" view that displays a user profile with the following
  fields:
  - [ ]: First Name
  - [ ]: Last Name
  - [ ]: Email
  - [ ]: Date of Birth
  - [ ]: Bio
  - [ ]: Avatar
- [ ]: Profile view has a link to edit the profile
- [ ]: Has an "Edit" view with:
  - [ ]: "/profile/edit" route
  - [ ]: Allows the user to edit the following profile fields:
    - [ ]: First Name
    - [ ]: Last Name
    - [ ]: Email
    - [ ]: Date of Birth
    - [ ]: Confirm Email
    - [ ]: Bio
    - [ ]: Avatar
- [ ]: Validates "Date of Birth" field, supporting the following formats:
  - [ ]: YYYY-MM-DD
  - [ ]: MM/DD/YYYY
  - [ ]: MM/DD/YY
- [ ]: Validates "Email" field:
  - [ ]: Check email matches confirm email
  - [ ]: Check email is valid format
- [ ]: Validates "Bio" field:
  - [ ]: Checks bio is at least 10 characters
  - [ ]: Properly escapes HTML formatting
- [ ]: Ability to upload and save user's avatar image
- [ ]: Has view "change-password":
  - [ ]: with route "/profile/change_password"
  - [ ]: that allows user to update their password using `User.set_password()` 
    then `User.save()`.
  - [ ]: form fields are `current_password`, `new_password`, `confirm_password`
- [ ]: Validates user input "password" fields:
  - [ ]: check old password is correct (using `User.check_password()`)
  - [ ]: new password matches the confirm password field
  - [ ]: follows the password policy:
    - [ ]: not same as existing password
    - [ ]: minimum length 14 characters
    - [ ]: must have uppercase character
    - [ ]: must have lowercase character
    - [ ]: must include one or more numerical digits
    - [ ]: must include special character
    - [ ]: cannot include username or user's first or last names
- [ ]: headings/font/forms are styled using CSS
- [ ]: Code complies with PEP8

### Extra Credit Features ###

- [ ]: Include additional form fields such as:
  - [ ]: city/state/country of residence
  - [ ]: favourite animal
  - [ ]: hobby
- [ ]: JavaScript used for a date dropdown for DoB validation feature
- [ ]: JS is used for text formatting for the Bio validation feature
- [ ]: Avatar has online image editor. Include the following functionality:
  - [ ]: rotate
  - [ ]: crop
  - [ ]: flip
- [ ]: Password strength "meter" displayed when validating passwords

Testing
-------

### [Test Running](https://docs.djangoproject.com/en/2.2/topics/testing/overview/#running-tests) ###

- Run all tests:
  ```console
   $ python manage.py test
   ```

- Run a single test suite:
  ```console
  $ python manage.py test accounts
  ```

- Run a single test file:
  ```console
  $ python manage.py test accounts.tests.test_models
  ```

- Run a single test case:
  ```console
  $ python manage.py test accounts.tests.test_models.UserProfileModelTest
  ```

- Run a single test method:
  ```console
  $ python manage.py test accounts.tests.test_models.UserProfileModelTest.test_userprofile_without_required_fields_is_invalid
  ```

### Coverage ###

- Run coverage:
  ```console
  $ coverage run manage.py test [the-app-to-test]
  ```

- Show the coverage report:
  ```console
  $ coverage report
  ```

- Erase the coverage report
  ```console
  $ coverage erase
  ```

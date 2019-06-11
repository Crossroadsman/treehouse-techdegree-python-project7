Project 7: User Profile With Django
===================================

Note: The minimum version of Python compatible with this project is 3.6 (December 2016)

Installation
------------

- Clone the repo
- Create and activate a venv
- To run the application install the required packages using `pip install -r requirements.txt`
- To be able to recreate coverage report you will also need to install the additional testing packages 
  using `pip install -r test-requirements.txt`

Included Users
--------------

### Super User ###

- User: `test@test.com`
- Password: `Project7-UserProfile`

### Demo User ###

- User: `demo@test.com`
- Password: `UPPERlower12345,./`

Feature Checklist
-----------------

### Base Features ###

- [x] : Uses provided base HTML/CSS
- [x] : Has Django model for user profile
- [x] : Has routes to:
  - [x] : Display a profile
  - [x] : Edit a profile
  - [x] : Change the password
- [x] : Has a "profile" view that displays a user profile with the following
  fields:
  - [x] : First Name
  - [x] : Last Name
  - [x] : Email
  - [x] : Date of Birth
  - [x] : Bio
  - [x] : Avatar
- [x] : Profile view has a link to edit the profile
- [x] : Has an "Edit" view with:
  - [x] : "/profile/edit" route
  - [x] : Allows the user to edit the following profile fields:
  - [x] : First Name
  - [x] : Last Name
  - [x] : Email
  - [x] : Date of Birth
  - [x] : Confirm Email
  - [x] : Bio
  - [x] : Avatar
- [x] : Validates "Date of Birth" field, supporting the following formats:
  - [x] : YYYY-MM-DD
  - [x] : MM/DD/YYYY
  - [x] : MM/DD/YY
- [x] : Validates "Email" field:
  - [x] : Check email matches confirm email
  - [x] : Check email is valid format
- [x] : Validates "Bio" field:
  - [x] : Checks bio is at least 10 characters
  - [x] : Properly escapes HTML formatting
- [x] : Ability to upload and save user's avatar image
- [x] : Has view "change-password":
  - [x] : with route "/profile/change_password"
  - [x] : that allows user to update their password using `User.set_password()` 
    then `User.save()`.
  - [x] : form fields are `current_password`, `new_password`, `confirm_password`
- [x] : Validates user input "password" fields:
  - [x] : check old password is correct (using `User.check_password()`)
  - [x] : new password matches the confirm password field
  - [x] : follows the password policy:
  - [x] : not same as existing password
  - [x] : minimum length 14 characters
  - [x] : must have uppercase character
  - [x] : must have lowercase character
  - [x] : must include one or more numerical digits
  - [x] : must include special character
  - [x] : cannot include username or user's first or last names
- [x] : headings/font/forms are styled using CSS
- [x] : Code complies with PEP8

### Extra Credit Features ###

- [x] : Include additional form fields such as:
  - [x] : city/state/country of residence
  - [x] : favourite animal
  - [x] : hobby
- [x] : JavaScript used for a date dropdown for DoB validation feature
- [x] : JS is used for text formatting for the Bio validation feature
- [x] : Avatar has online image editor. Include the following functionality:
  - [x] : rotate
  - [x] : crop
  - [x] : flip
- [x] : Password strength "meter" displayed when validating passwords

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

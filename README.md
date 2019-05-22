Project 7: User Profile With Django
===================================

Password:
Project7-UserProfile

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

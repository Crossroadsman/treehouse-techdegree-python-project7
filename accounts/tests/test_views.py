from django.contrib.auth import get_user_model, get_user
User = get_user_model()
from django.test import Client, TestCase
from django.urls import resolve, reverse

from accounts.views import (sign_in, sign_up)


class AccountViewsTestCase(TestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        self.abstract = True
        self.url = '/accounts/'
        self.name = 'accounts:'
        self.status_code = 200
        self.template = 'accounts/'
        self.target_view = None

        self.client = Client()

    # Test Methods
    # ------------
    def test_url_resolves_to_correct_view(self):
        """Ensure that expected URLs resolve to their associated views"""

        if self.abstract:
            return

        resolved_view = resolve(self.url).func

        self.assertEqual(resolved_view, self.target_view)

    def test_view_associated_with_correct_name(self):
        if self.abstract:
            return

        response = self.client.get(reverse(self.name))

        self.assertEqual(response.status_code, self.status_code)

    def test_view_renders_correct_template(self):
        if self.abstract:
            return
    
        response = self.client.get(reverse(self.name))
        
        self.assertTemplateUsed(response, self.template)


class SignUpViewTest(AccountViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'sign_up'
        self.template += 'sign_up.html'
        self.url += 'sign_up'
        self.target_view = sign_up

    def test_new_user_is_created_after_correct_sign_up(self):
        test_email = "alicesmith@test.com"
        test_password = "Testing123xyz!;,"

        before_users_count = User.objects.all().count()

        self.client.post(
            reverse(self.name),
            data={
                'email': test_email,
                'password1': test_password,
                'password2': test_password
            }
        )

        after_users_count = User.objects.all().count()

        new_user_count = after_users_count - before_users_count
        self.assertEqual(new_user_count, 1)

    def test_duplicate_user_is_not_created_after_sign_up(self):
        test_email = "alicesmith@test.com"
        test_password = "Testing123xyz!;,"

        existing_user = User.objects.create_user(test_email, test_password)

        before_users_count = User.objects.all().count()

        self.client.post(
            reverse(self.name),
            data={
                'email': test_email,
                'password1': test_password,
                'password2': test_password
            }
        )

        after_users_count = User.objects.all().count()

        self.assertEqual(before_users_count, after_users_count)


class SignInViewTest(AccountViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'sign_in'
        self.template += 'sign_in.html'
        self.url += 'sign_in'
        self.target_view = sign_in

        self.test_credentials = {
            'email': "alicesmith@test.com",
            'password': "Testing123xyz!,."
        }
        self.test_user = User.objects.create_user(**self.test_credentials)
    
    def test_specified_user_is_logged_in_after_correct_sign_in(self):
        
        user_before_login = get_user(self.client)
        self.assertFalse(user_before_login.is_authenticated)

        # The authentication form always calls the identity field 'username'
        # even though we've called it 'email' on our model
        self.client.post(
            reverse(self.name),
            data={
                'username': self.test_credentials['email'],
                'password': self.test_credentials['password']
            }
        )

        user_after_login = get_user(self.client)
        self.assertTrue(user_after_login.is_authenticated)

    def test_specified_user_is_not_logged_in_after_incorrect_username(self):
        bad_username = "bobjones@test.com"

        user_before_login = get_user(self.client)
        self.assertFalse(user_before_login.is_authenticated)

        # The authentication form always calls the identity field 'username'
        # even though we've called it 'email' on our model
        self.client.post(
            reverse(self.name),
            data={
                'username': bad_username,
                'password': self.test_credentials['password']
            }
        )

        user_after_login = get_user(self.client)
        self.assertFalse(user_after_login.is_authenticated)

    def test_specified_user_is_not_logged_in_after_incorrect_password(self):
        bad_password = "BadPass123xyz!.,"

        user_before_login = get_user(self.client)
        self.assertFalse(user_before_login.is_authenticated)

        # The authentication form always calls the identity field 'username'
        # even though we've called it 'email' on our model
        self.client.post(
            reverse(self.name),
            data={
                'username': self.test_credentials['email'],
                'password': bad_password
            }
        )

        user_after_login = get_user(self.client)
        self.assertFalse(user_after_login.is_authenticated)

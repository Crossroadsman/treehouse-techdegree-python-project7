from django.test import TestCase
from django.urls import resolve

from accounts.views import (sign_in, sign_up, sign_out, profile, 
                            edit_profile, bio, change_password)


class AccountViewsTestCase(TestCase):

    def setUp(self):
        self.abstract = True
        self.url = '/accounts/'
        self.target_view = None
    
    def test_url_resolves_to_correct_view(self):
        """Ensure that expected URLs resolve to their associated views"""

        if self.abstract:
            return

        resolved_view = resolve(self.url).func

        self.assertEqual(resolved_view, self.target_view)


class SignInViewTest(AccountViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'sign_in'
        self.target_view = sign_in


class SignUpViewTest(AccountViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'sign_up'
        self.target_view = sign_up


class SignOutViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'sign_out'
        self.target_view = sign_out


class ProfileViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'profile'
        self.target_view = profile


class EditProfileViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'profile/edit'
        self.target_view = edit_profile


class BioViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'bio'
        self.target_view = bio


class ChangePasswordViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.url += 'profile/change-password'
        self.target_view = change_password

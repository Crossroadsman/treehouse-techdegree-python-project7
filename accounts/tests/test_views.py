import unittest

from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import Client, RequestFactory, TestCase
from django.urls import resolve, reverse

from accounts.models import UserProfile
from accounts.views import (sign_in, sign_up, sign_out, profile, 
                            edit_profile, bio, change_password)


class AccountViewsTestCase(TestCase):

    def setUp(self):
        self.abstract = True
        self.url = '/accounts/'
        self.name = 'accounts:'
        self.status_code = 200
        self.template = 'accounts/'
        self.target_view = None

        self.client = Client()
    
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



class SignInViewTest(AccountViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'sign_in'
        self.template += 'sign_in.html'
        self.url += 'sign_in'
        self.target_view = sign_in


class SignUpViewTest(AccountViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'sign_up'
        self.template += 'sign_up.html'
        self.url += 'sign_up'
        self.target_view = sign_up


class SignOutViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'sign_out'
        self.status_code = 302  # This view just redirects
        self.template += 'sign_out.html'
        self.url += 'sign_out'
        self.target_view = sign_out

    @unittest.skip("no template to render, just redirects")
    def test_view_renders_correct_template(self):
        pass


class ProfileViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'profile'
        self.template += 'profile.html'
        self.url += 'profile'
        self.target_view = profile

        self.request_factory = RequestFactory()
        self.user = User.objects.create(email="testuser@test.com")

    def test_view_associated_with_correct_name(self):
        self.userprofile = UserProfile.objects.create(
            user=self.user,
            date_of_birth=date(1977, 5, 25),
            bio="this is a string with more than 10 characters"
        )

        request = self.request_factory.get(reverse(self.name))
        request.user = self.user
        response = self.target_view(request)

        self.assertEqual(response.status_code, self.status_code)

    def test_view_renders_correct_template(self):
        self.userprofile = UserProfile.objects.create(
            user=self.user,
            date_of_birth=date(1977, 5, 25),
            bio="this is a string with more than 10 characters"
        )

        request = self.request_factory.get(reverse(self.name))
        request.user = self.user
        response = self.target_view(request)

        self.assertTemplateUsed(response, self.template)

    def test_redirects_to_editprofile_if_no_userprofile(self):
        redirect_target = '/accounts/edit_profile'

        request = self.request_factory.get(reverse(self.name))
        request.user = self.user
        response = self.target_view(request)

        self.assertRedirects(response, redirect_target)


class EditProfileViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'edit_profile'
        self.template += 'edit_profile.html'
        self.url += 'profile/edit'
        self.target_view = edit_profile


class BioViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'bio'
        self.template += 'bio.html'
        self.url += 'bio'
        self.target_view = bio


class ChangePasswordViewTest(AccountViewsTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'change_password'
        self.url += 'profile/change-password'
        self.target_view = change_password

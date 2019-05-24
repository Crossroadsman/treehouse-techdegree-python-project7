from datetime import date

import unittest

from django.contrib.auth import get_user_model
User = get_user_model()
from django.template.loader import render_to_string
from django.test import Client, RequestFactory, TestCase
from django.urls import resolve, reverse

from accounts.models import UserProfile
from accounts.views import (sign_in, sign_up, sign_out, profile, 
                            edit_profile, bio, change_password)


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

### Move AccountViewsWithUserTestCase definition here later ###


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

class AccountViewsWithUserTestCase(AccountViewsTestCase):
    
    # setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()

        # To provide a user we need to build a custom request using
        # RequestFactory
        self.request_factory = RequestFactory()
        self.user = User.objects.create(email="alicesmith@test.com")
        # TODO: ACTUALLY, it looks like we can do this:
        # self.user = User.objects.create(email="alicesmith@test.com")
        # self.client.force_login(self.user)
        # see:
        # https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.Client.force_login

        # Using ReqeustFactory instead of client, we can't use
        # assertTemplateUsed. Therefore we'll check that we've rendered
        # the correct template by testing the rendered <title> element
        self.template_title = ''

    # Helper Methods
    # --------------
    def create_userprofile(self, user):
        userprofile = UserProfile.objects.create(
            user=user,
            date_of_birth=date(1977, 5, 25),
            bio="this is a string with more than 10 characters"
        )
        return userprofile

    def create_optional_userprofile_data(self):
        """One a user is active and has a userprofile, populate the
        optional fields with some standardised test data

        returns the dictionary of test data for use in asserts
        """
        test_profile_data = {
            'given_name': 'alice',
            'family_name': 'smith',
            'city': 'anytown',
            'state': 'anystate',
            'country': 'anycountry',
            'favourite_animal': 'dog',
            'hobby': 'dog snuggling',
            'favourite_fountain_pen': 'pilot metropolitan'
        }
        self.userprofile.given_name = test_profile_data['given_name']
        self.userprofile.family_name = test_profile_data['family_name']
        self.userprofile.city = test_profile_data['city']
        self.userprofile.state = test_profile_data['state']
        self.userprofile.country = test_profile_data['country']
        self.userprofile.favourite_animal = test_profile_data['favourite_animal']
        self.userprofile.hobby = test_profile_data['hobby']
        self.userprofile.favourite_fountain_pen = test_profile_data['favourite_fountain_pen']
        self.userprofile.save()

        return test_profile_data

    def make_request_for_current_user(self, method='get', redirect=None, data=None):
        if method.lower() == 'post':
            request = self.request_factory.post(
                redirect,
                data=data
            )
        else:  # 'get'
            request = self.request_factory.get(reverse(self.name))
        request.user = self.user
        response = self.target_view(request)
        return response

    def get_title_text(self, response):
        decoded = response.content.decode()
        start = decoded.find('<title>') + 7
        end = decoded.find('</title>')
        title = decoded[start:end]
        return title


    # Test Methods
    # ------------
    def test_view_associated_with_correct_name(self):
        self.userprofile = self.create_userprofile(self.user)

        response = self.make_request_for_current_user()

        self.assertEqual(response.status_code, self.status_code)

    def test_view_renders_correct_template(self):
        self.userprofile = self.create_userprofile(self.user)

        response = self.make_request_for_current_user()

        title = self.get_title_text(response)

        self.assertEqual(self.template_title, title)

    
class ProfileViewTest(AccountViewsWithUserTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'profile'
        self.template_title = 'Profile | '
        self.url += 'profile'
        self.target_view = profile

    def test_redirects_to_editprofile_if_no_userprofile(self):
        redirect_target = '/accounts/edit_profile'

        response = self.make_request_for_current_user()
        self.assertEqual(response.status_code, 302)

        # DEBUG
        print("==== RESPONSE ====")
        print("---- status ----")
        print(response.status_code)
        print("---- end status ----")
        print("---- content (utf-8 encoded bytestring) ----")
        print(response.content)
        print("---- end content ----")
        print("---- content (decoded) ----")
        print(response.content.decode())
        print("---- end content ----")
        print("==== END RESPONSE ====")

        self.assertRedirects(response, redirect_target)

    def test_displays_correct_profile_data(self):
        
        self.userprofile = self.create_userprofile(self.user)
        test_profile_data = self.create_optional_userprofile_data()
        

        response = self.make_request_for_current_user()

        # You can compare the raw bytes content and decoded content by
        # uncommenting the folllowing code:
        # print("==== RESPONSE ====")
        # print("---- content (utf-8 encoded bytestring) ----")
        # print(response.content)
        # print("---- end content ----")
        # print("---- content (decoded) ----")
        # print(response.content.decode())
        # print("---- end content ----")
        # print("==== END RESPONSE ====")

        # Django provides assertContains: like assertIn but automatically
        # handles encoding/decoding between response.content bytestring
        # and regular python strings (saving us from using the decode() method
        # on the response.content bytestring)
        for value in test_profile_data.values():
            self.assertContains(response, value)


class EditProfileViewTest(AccountViewsWithUserTestCase):
    
    # Setup and Teardown
    # ------------------
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'edit_profile'
        self.template_title = 'Edit Profile | '
        self.url += 'profile/edit'
        self.target_view = edit_profile

    # Test Methods
    # ------------    
    def test_view_renders_correct_template_if_POST_invalid(self):
        # for POSTs with validation errors
        self.userprofile = self.create_userprofile(self.user)
        
        test_userform = {}
        test_profileform = {}
        test_postdata = {**test_userform, **test_profileform}

        response = self.make_request_for_current_user(
            method='post',
            redirect=reverse(self.name),
            data=test_postdata
        )

        # DEBUG
        # print("==== RESPONSE (POST INVALID)====")
        # print("---- content (utf-8 encoded bytestring) ----")
        # print(response.content)
        # print("---- end content ----")
        # print("---- content (decoded) ----")
        # print(response.content.decode())
        # print("---- end content ----")
        # print("==== END RESPONSE ====")

        title = self.get_title_text(response)

        self.assertEqual(self.template_title, title)

    def test_redirects_to_profile_if_valid_POST(self):
        # for valid POSTs
        redirect_target = '/accounts/profile'

        # create data for POSTing
        user_data = {
            'email': self.user.email,
            'confirm_email': self.user.email
        }
        required_profile_data = {
            'dob': self.userprofile.date_of_birth,
            'bio': self.userprofile.bio
        }
        optional_profile_data = self.create_optional_userprofile_data()
        test_fields = {**user_data, **required_profile_data, **optional_profile_data}

        response = self.make_request_for_current_user(
            method='post',
            redirect=reverse(self.name),
            data=test_fields
        )

        self.assertRedirects(response, redirect_target)

    def test_view_populates_form_with_existing_profile_data(self):

        # Create a user (done as part of setUp)
        # Associate a userprofile
        self.userprofile = self.create_userprofile(self.user)

        # Arrange test data and create initial userprofile data
        # Field list:
        # email (user)
        #
        # confirm email
        #
        # dob
        # first name
        # last name
        # bio
        # city
        # state
        # country
        # favourite animal
        # hobby
        # favourite fountain pen
        user_data = {
            'email': self.user.email,
            'confirm_email': self.user.email
        }
        required_profile_data = {
            'dob': self.userprofile.date_of_birth,
            'bio': self.userprofile.bio
        }
        optional_profile_data = self.create_optional_userprofile_data()
        test_fields = {**user_data, **required_profile_data, **optional_profile_data}

        # Create a GET request with that user
        response = self.make_request_for_current_user()

        # DEBUG: Review the response
        # print("==== RESPONSE ====")
        # print("---- content (utf-8 encoded bytestring) ----")
        # print(response.content)
        # print("---- end content ----")
        # print("---- content (decoded) ----")
        # print(response.content.decode())
        # print("---- end content ----")
        # print("==== END RESPONSE ====")

        # Capture the output from the page
        decoded = response.content.decode()

        # Assert that the form fields are populated with the values
        for field, value in test_fields.items():
            self.assertContains(decoded, f'id_{field}')
            self.assertContains(decoded, f'value="{value}"')

    def test_view_updates_models_with_profile_changes(self):
        # Create a user (done as part of setUp)
        # Associate a userprofile
        self.userprofile = self.create_userprofile(self.user)
        user_id = self.user.id
        
        # Create initial userprofile data
        self.create_initial_userprofile_data()

        # Define new userprofile data
        new_user_data = {
            'email': 'bobjones@test.com',
            'confirm_email': 'bobjones@test.com',
        }
        new_profile_data = {
            'date_of_birth': date(1980, 5, 17),
            'bio': 'This is a different string of at least 10 characters',
            'given_name': 'bob',
            'family_name': 'jones',
            'city': 'othertown',
            'state': 'otherstate',
            'country': 'othercountry',
            'favourite_animal': 'also dog',
            'hobby': 'dog cuddling',
            'favourite_fountain_pen': 'lamy vista'
        }
        new_data_combined = {**new_user_data, **new_profile_data}

        # Build the request with the changes, and then POST it

        # POST the form
        # request = self.request_factory.post(reverse(self.name), data=new_data_combined)
        # request.user = self.user
        # response = self.target_view(request)
        response = self.make_request_for_current_user(
            method='post',
            redirect=reverse(self.name),
            data=new_data_combined
        )

        # DEBUG: Review the response
        # print("==== RESPONSE ====")
        # print("---- content (utf-8 encoded bytestring) ----")
        # print(response.content)
        # print("---- end content ----")
        # print("---- content (decoded) ----")
        # print(response.content.decode())
        # print("---- end content ----")
        # print("==== END RESPONSE ====")
        
        # load the model(s)
        user = User.objects.get(pk=user_id)
        profile = user.userprofile

        # confirm model data matches submitted changes
        self.assertEqual(user.email, new_user_data['email'])

        self.assertEqual(profile.given_name, new_profile_data['given_name'])
        self.assertEqual(profile.family_name, new_profile_data['family_name'])
        self.assertEqual(profile.city, new_profile_data['city'])
        self.assertEqual(profile.state, new_profile_data['state'])
        self.assertEqual(profile.country, new_profile_data['country'])
        self.assertEqual(profile.favourite_animal, new_profile_data['favourite_animal'])
        self.assertEqual(profile.hobby, new_profile_data['hobby'])
        self.assertEqual(profile.favourite_fountain_pen, new_profile_data['favourite_fountain_pen'])


class BioViewTest(AccountViewsWithUserTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'bio'
        self.template_title = 'Bio | '
        self.url += 'bio'
        self.target_view = bio


class ChangePasswordViewTest(AccountViewsWithUserTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'change_password'
        self.template_title = 'Password Change'
        self.url += 'profile/change-password'
        self.target_view = change_password

    # renders view on GET
    # (included with parent TestCase)

    # renders view on invalid POST
    # (see edit profile view tests)
    def test_view_renders_correct_template_on_invalid_POST(self):
        self.fail("implement me")

    # redirect on valid POST
    # (see edit profile view tests)
    def test_view_redirects_to_correct_view_on_valid_POST(self):
        self.fail("implement me")

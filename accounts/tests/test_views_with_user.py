from datetime import date

import unittest

from django.contrib.auth import get_user_model, get_user
User = get_user_model()
from django.test import Client, RequestFactory
from django.urls import reverse

from accounts.models import UserProfile
from accounts.views import (sign_out, profile, 
                            edit_profile, bio, change_password)
from accounts.tests.test_views import AccountViewsTestCase


class AccountViewsWithUserTestCase(AccountViewsTestCase):
    
    # setup and teardown
    # ------------------
    def setUp(self):
        super().setUp()

        self.test_credentials = {
            'email': "alicesmith@test.com",
            'password': "Testing123xyz!,."
        }
        self.user = User.objects.create_user(**self.test_credentials)

        self.client.force_login(self.user)
        # see:
        # https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.Client.force_login

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
        """Once a user is active and has a userprofile, populate the
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

    def get_title_text(self, response):
        decoded = response.content.decode()
        start = decoded.find('<title>') + 7
        end = decoded.find('</title>')
        title = decoded[start:end]
        return title


class SignOutViewTest(AccountViewsWithUserTestCase):
    
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

    def test_specified_user_is_logged_out_after_sign_out(self):

        user_before_logout = get_user(self.client)
        self.assertTrue(user_before_logout.is_authenticated)

        self.client.get(reverse(self.name))
        
        user_after_logout = get_user(self.client)
        self.assertFalse(user_after_logout.is_authenticated)


class ProfileViewTest(AccountViewsWithUserTestCase):
    
    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'profile'
        self.template += 'profile.html'
        self.url += 'profile'
        self.target_view = profile

    def test_view_renders_correct_template(self):
        # if a userprofile exists
        self.create_userprofile(self.user)
        super().test_view_renders_correct_template()

    def test_view_associated_with_correct_name(self):
        # if a userprofile exists
        self.create_userprofile(self.user)
        super().test_view_associated_with_correct_name()


    def test_redirects_to_editprofile_if_no_userprofile(self):
        redirect_target = '/accounts/profile/edit'

        response = self.client.get(reverse(self.name))

        self.assertRedirects(response, redirect_target)

    def test_displays_correct_profile_data(self):
        
        self.userprofile = self.create_userprofile(self.user)
        test_profile_data = self.create_optional_userprofile_data()

        response = self.client.get(reverse(self.name))

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
        self.template += 'edit_profile.html'
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

        response = self.client.post(
            reverse(self.name),
            data=test_postdata
        )

        self.assertTemplateUsed(response, self.template)

    def test_redirects_to_profile_if_valid_POST(self):
        # for valid POSTs
        redirect_target = '/accounts/profile'

        # create data for POSTing
        postdata = {
            'email': self.user.email,
            'confirm_email': self.user.email,
            'dob': self.userprofile.date_of_birth,
            'bio': self.userprofile.bio
        }

        response = self.client.post(
            reverse(self.name),
            data=postdata
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
            'date_of_birth': self.userprofile.date_of_birth,
        }
        optional_profile_data = self.create_optional_userprofile_data()
        test_fields = {**user_data, **required_profile_data, **optional_profile_data}

        # Create a GET request with that user
        response = self.client.get(reverse(self.name))

        # Assert that the form fields are populated with the values
        for field, value in test_fields.items():
            self.assertContains(response, f'id_{field}')
            self.assertContains(response, f'value="{value}"')
        self.assertContains(response, f'id_bio')
        self.assertContains(response, self.userprofile.bio)

    def test_view_updates_models_with_profile_changes(self):
        # Create a user (done as part of setUp)
        # Associate a userprofile
        self.userprofile = self.create_userprofile(self.user)
        user_id = self.user.id
        
        # Create optional userprofile data
        self.create_optional_userprofile_data()

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
        response = self.client.post(
            reverse(self.name),
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
        # print("---- redirect chain ----")
        # # only works if follow=True
        # # print(response.redirect_chain)
        # print("---- end redirect chain ----")
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
        self.template += 'change_password.html'
        self.url += 'profile/change-password'
        self.target_view = change_password

    # renders view on GET
    # (included with parent TestCase)

    # renders view on invalid POST
    def test_view_renders_correct_template_on_invalid_POST(self):

        wrong_password = 'InvalidPass123456,.'
        
        response = self.client.post(
            reverse(self.name),
            data={
                'old_password': wrong_password,
                'new_password1': self.test_credentials['password'],
                'new_password2': self.test_credentials['password']
            }
        )
        
        self.assertTemplateUsed(response, self.template)

    # redirect on valid POST to profile view
    def test_view_redirects_to_correct_view_on_valid_POST(self):

        new_valid_password = 'SomeRandomString9876,.'
        redirect_target = '/accounts/profile'

        # IMPORTANT
        # ---------
        # Per the specifications, only bio and dob are required profile
        # fields.
        # If we just create those fields, the other text fields will be 
        # created with blank strings (e.g., first name and last name).
        # The password validator will then fail any new password because
        # any string contains the empty string.
        # TODO
        # For now, we'll create a full userprofile to get this test to pass
        # then we'll figure out how to improve the behaviour of the password
        # validator
        self.userprofile = self.create_userprofile(self.user)
        self.create_optional_userprofile_data()
                
        response = self.client.post(
            reverse(self.name),
            data={
                'old_password': self.test_credentials['password'],
                'new_password1': new_valid_password,
                'new_password2': new_valid_password
            },
        )

        self.assertRedirects(response, redirect_target)

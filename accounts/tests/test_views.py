from datetime import date

from unittest.mock import Mock

from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.utils import IntegrityError
from django.test import TestCase, TransactionTestCase

from accounts.models import user_avatar_path, UserProfile


class UserAvatarPathFunctionTest(TestCase):

    def test_function_returns_correct_path(self):
        mock_user = Mock(user_id=1)
        test_filename = "test_image.jpg"
        expected_output = "avatars/1.jpg"

        avatar_path = user_avatar_path(mock_user, test_filename)

        self.assertEqual(avatar_path, expected_output)


# We use TransactionTestCase instead of the more common TestCase for the 
# following test because the way that the test database rolls back when
# using TestCase causes errors when trying to iterate through the invalid
# UserProfiles. See more detailed description of the difference between
# TestCase and TransactionTestCase at:
# https://docs.djangoproject.com/en/1.11/topics/testing/tools/#transactiontestcase
class UserProfileModelTest(TransactionTestCase):


    def setUp(self):
        self.valid_user = User.objects.create(email="test@test.com")
        self.valid_dob = date(1977, 5, 25)
        self.valid_bio = "this is a string with more than 10 characters"

    def test_userprofile_without_required_fields_is_invalid(self):

        no_user_model = UserProfile(
            user=None,
            date_of_birth=self.valid_dob,
            bio=self.valid_bio
        )

        no_dob_model = UserProfile(
            user=self.valid_user,
            date_of_birth=None,
            bio=self.valid_bio
        )

        second_valid_user = User.objects.create(email="test2@test.com")
        no_bio_model = UserProfile(
            user=second_valid_user,
            date_of_birth=self.valid_dob,
            bio=None
        )

        for model in [
            no_user_model,
            no_dob_model,
            no_bio_model,
        ]:
            with self.assertRaises(IntegrityError):
                model.save()

    def test_userprofile_is_related_to_user(self):
        test_profile = UserProfile.objects.create(
            user=self.valid_user,
            date_of_birth=self.valid_dob,
            bio=self.valid_bio
        )

        self.assertIs(test_profile, self.valid_user.userprofile)

    def test_userprofile_string_representation_is_name_andor_email(self):
        """if a part of the name is available, e.g., 'Alice', the
        representation should be the available name then email in parens,
        e.g., 'Alice (alice@test.com)'. If no name, just email, e.g., 
        'alice@test.com'. Surnames are in all-caps
        """
        test_data = [
            {
                'email': 'noname@test.com', 
                'expected_str': 'noname@test.com'
            },
            {
                'email': 'alice@test.com', 
                'given_name': 'alice',
                'expected_str': 'alice (alice@test.com)',
            },
            {
                'email': 'smith@test.com', 
                'family_name': 'smith',
                'expected_str': 'SMITH (smith@test.com)',
            },
            {
                'email': 'alicesmith@test.com', 
                'given_name': 'alice', 
                'family_name': 'smith',
                'expected_str': 'alice SMITH (alicesmith@test.com)',
            },
        ]
        for user in test_data:
            User.objects.create(email=user['email']),
            u = User.objects.get(email=user['email'])

            UserProfile.objects.create(
                user=u,
                date_of_birth=self.valid_dob,
                bio=self.valid_bio,
                given_name = user.get('given_name', ''),
                family_name = user.get('family_name', ''),
            )

        for user in test_data:
            u = User.objects.get(email=user['email'])
            profile = u.userprofile
            self.assertEqual(user['expected_str'], str(profile))
            

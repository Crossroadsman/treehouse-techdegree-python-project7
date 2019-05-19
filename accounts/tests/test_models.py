from datetime import date

from unittest.mock import Mock

from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.models import user_avatar_path, UserProfile


class UserAvatarPathFunctionTest(TestCase):

    def test_function_returns_correct_path(self):
        mock_user = Mock(user_id=1)
        test_filename = "test_image.jpg"
        expected_output = "avatars/1.jpg"

        avatar_path = user_avatar_path(mock_user, test_filename)

        self.assertEqual(avatar_path, expected_output)


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.valid_user = User(email="test@test.com")
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

        no_bio_model = UserProfile(
            user=self.valid_user,
            date_of_birth=self.valid_dob,
            bio=None
        )

        for model in [
            no_user_model,
        ]:
            with self.assertRaises(IntegrityError):
                model.save()

        for model in [
            no_dob_model,
            no_bio_model,
        ]:
            with self.assertRaises(ValidationError):
                model.save()

                # Django's validation in save behaviour is counter-intuitive.
                # Django will not try to enforce any constraints not supported
                # by the DB. For example, SQLite doesn't support a constraint
                # equivalent to 'blank=False' (the default for TextField 
                # objects).
                # We can force full validation by manually calling 
                # Model.full_clean().
                # Note this turns the constraint into an application level
                # constraint so the violation is ValidationError whereas a
                # true constraint violation on save is an IntegrityError
                model.full_clean()


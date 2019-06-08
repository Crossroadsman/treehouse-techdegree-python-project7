from datetime import date
from io import BytesIO
import json
import unittest

from django.contrib.auth import get_user_model, get_user
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import resolve, reverse

from PIL import Image

from accounts.models import UserProfile
from image_edit.views import cropper, upload_image


User = get_user_model()


class ImageEditViewsTestCase(TestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        self.abstract = True
        self.url = '/avatar/'
        self.name = 'image_edit:'
        self.status_code = 200
        self.template = 'image_edit/'
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


class CropperViewTestCase(ImageEditViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'cropper'
        self.template += 'cropper.html'
        self.target_view = cropper
        self.url += ''


class UploadImageViewTestCase(ImageEditViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'upload_image'
        self.target_view = upload_image
        self.url += 'upload_image'

        test_user_credentials = {
            'email': 'alicesmith@test.com',
            'password': 'UPPERlower123456,./!@#'
        }
        test_userprofile_values = {
            'date_of_birth': date(1977, 5, 25),
            'bio': 'This is a test string of more than 10 characters'
        }

        # create a user
        self.test_user = User.objects.create_user(**test_user_credentials)

        # create a minimal user profile
        UserProfile.objects.create(
            user=self.test_user,
            **test_userprofile_values
        )

        # log in our test user
        self.client.force_login(self.test_user)

        # create an image file (or image data)
        test_image_file = self.make_image_file()
        # test_image_data = self.make_image_data()

        # Regardless of whether we are using image data or an image file
        # as the form payload, we will need to seek the object to the start
        # of file before passing it into the form, otherwise the whole file
        # will not be sent and PIL won't be able to interpret the file as
        # an image.
        test_image_file.seek(0)
        # test_image_data.seek(0)

        # create form data
        self.form_data = {'image': test_image_file}
        # self.form_data = {'image': test_image_data}

    def make_image_data(self):
        """Creates an in-memory bytes stream containing image data and
        returns it
        """

        # Create an in-memory binary stream object
        image_data = BytesIO()

        # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
        image_settings = {
            'mode': "RGB",
            'size': (128, 128)
        }
        # `fp` : A filename (string), pathlib.Path object or file object
        # `format` : If None, format is inferred from file extension
        #      (explicitly setting format is required if using a file object
        #      instead of a filename)
        stream_settings = {
            'fp': image_data,
            'format': 'JPEG',

        }
        image_object = Image.new(**image_settings)
        image_object.save(**stream_settings)  # write the image data to stream

        return image_data

    def make_image_file(self):
        """Creates an in-memory image file and returns it"""

        # Note that for our particular test scenario, we don't need to
        # create a file: the form can accept the bytes data directly. However,
        # we're illustrating how we would go from a bytes object to a Django
        # file object (which is a thin wrapper around a Python file object)
        # in case we need to be able to work with 'real' files later.
        image_data = self.make_image_data()

        # Note, when getting the string representation of the file it is
        # described as:
        # `test_file.jpg (text/plain)`
        # It doesn't seem to be an issue that Django thinks it is a text file:
        # Running readlines on the file reveals it to be a binary file
        # And PIL is able to read the file without complaint.
        image_file = SimpleUploadedFile('test_file.jpg', image_data.getvalue())

        return image_file

    @unittest.skip("never renders template, just makes json httpResponse")
    def test_view_renders_correct_template(self):
        pass

    def test_view_returns_valid_json_response(self):
        expected_response = {
            'status': 1,
            'message': "Ok",
            'url': reverse('accounts:profile'),
        }

        # make POST request
        response = self.client.post(
            reverse(self.name),
            self.form_data
        )

        decoded = response.content.decode()  # a flat string of JSON
        response_dict = json.loads(decoded)

        for key in expected_response.keys():
            self.assertEqual(
                expected_response[key],
                response_dict[key]
            )

    def test_view_uploads_image(self):

        # make POST request
        self.client.post(
            reverse(self.name),
            self.form_data
        )

        self.assertIsNotNone(self.test_user.userprofile.avatar)

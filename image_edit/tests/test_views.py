import unittest

from django.test import Client, TestCase
from django.urls import resolve, reverse

from image_edit.views import cropper, upload_image


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

    @unittest.skip("never renders template, just makes json httpResponse")
    def test_view_renders_correct_template(self):
        pass

    def test_view_returns_valid_json_response(self):
        expected_response = {
            'status': 1,
            'message': "Ok",
            'url': reverse('accounts:profile'),
        }
        
        self.fail("implement me")

    def test_view_uploads_image(self):
        self.fail("implement me")

from django.test import Client, TestCase
from django.urls import resolve, reverse

from project_7.views import home


class Project7ViewsTestCase(TestCase):

    # Setup and teardown
    # ------------------
    def setUp(self):
        self.abstract = True
        self.url = '/'
        self.name = ''
        self.status_code = 200
        self.template = ''
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


class HomeViewTestCase(Project7ViewsTestCase):

    def setUp(self):
        super().setUp()
        self.abstract = False
        self.name += 'home'
        self.target_view = home
        self.template += 'home.html'

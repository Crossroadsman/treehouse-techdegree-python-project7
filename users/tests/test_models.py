from django.test import TestCase

from users.models import P7UserManager, P7User


class P7UserTestCase(TestCase):

    def setUp(self):
        self.test_user = P7User.objects.create_user(
            email='alicesmith@test.com',
            password='UPPERlower123456,./!@#'
        )

    def test_user_has_all_required_values(self):

        # Test has the required fields for the custom user model
        # (including ones required by Django)
        self.assertEqual(self.test_user.email, "alicesmith@test.com")
        self.assertEqual(self.test_user.is_active, True)
        self.assertEqual(self.test_user.is_staff, False)
        self.assertEqual(self.test_user.is_superuser, False)

        # Test existence of MTM relations to Group/Permission
        # non-existent attributes will raise AttributeError
        self.test_user.user_permissions.all()
        self.test_user.groups.all()

        # Test email is set to be the username field
        self.assertEqual(self.test_user.USERNAME_FIELD, 'email')

        # Test no other fields are required for creating superuser
        self.assertEqual(self.test_user.REQUIRED_FIELDS, [])

    def test_hasperm_is_implemented(self):

        # will fail with AttributeError if not implemented
        # or assertion error if the method is implemented but the wrong
        # result comes back
        self.assertFalse(self.test_user.has_perm('users.some_permission'))

    def test_hasmoduleperms_is_implemented(self):

        # will fail with AttributeError if not implemented
        # or assertion error if the method is implemented but the wrong
        # result comes back
        self.assertFalse(self.test_user.has_module_perms('users'))


class P7UserManagerTestCase(TestCase):

    def setUp(self):
        self.manager = P7User.objects

    def test_createuser_with_valid_credentials_creates_user(self):

        p7users = self.manager.all()
        self.assertEqual(p7users.count(), 0)

        self.manager.create_user(
            email='alicesmith@test.com',
            password='UPPERlower123456,./!@#'
        )

        test_user = self.manager.all()[0]
        self.assertEqual(test_user.email, 'alicesmith@test.com')

    def test_createuser_without_email_raises_error(self):

        with self.assertRaises(TypeError):
            self.manager.create_user(
                password='UPPERlower123456,./!@#'
            )

    def test_createsuperuser_with_valid_credentials_creates_superuser(self):

        p7users = self.manager.all()
        self.assertEqual(p7users.count(), 0)

        self.manager.create_superuser(
            email='alicesmith@test.com',
            password='UPPERlower123456,./!@#'
        )

        test_user = self.manager.all()[0]
        self.assertEqual(test_user.email, 'alicesmith@test.com')

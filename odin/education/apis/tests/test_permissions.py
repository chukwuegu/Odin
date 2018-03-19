from test_plus import TestCase
from odin.education.apis.permissions import IsStudentPermission
from odin.users.factories import BaseUserFactory
from odin.education.models import Student


def make_mock_object(**kwargs):
    return type('', (object, ), kwargs)


class TestIsStudenPermission(TestCase):
    def setUp(self):
        self.user = BaseUserFactory()
        self.request = make_mock_object(user=self.user)

    def test_permission_if_user_is_student(self):
        student = Student.objects.create_from_user(self.user)
        student.save()

        permissions = IsStudentPermission()

        self.assertTrue(permissions.has_permission(self.request, None))

    def test_permission_if_user_is_not_student(self):
        permissions = IsStudentPermission()

        self.assertFalse(permissions.has_permission(self.request, None))
# Third Party Stuff
from django.test import TestCase

# milife-back Stuff
from milife_back.users.models import User


class UserModelTestCase(TestCase):

    def test_create_user(self):
        u = User.objects.create_user(email='f@F.com', password='abc', first_name="F", last_name='B')
        assert u.is_active is True
        assert u.is_staff is False
        assert u.is_superuser is False

        assert u.email == 'f@f.com', "Email field is case sensitive"
        u.email = 'fF.com'
        assert u.email != 'fF.com', "Email field is not validated"
        u.email = 'f@Fcom'
        assert u.email != 'f@Fcom', "Email field is not validated"

        assert u.get_full_name() == 'F B'
        assert u.get_short_name() == 'F'
        assert str(u) == str(u.id)

    def test_create_super_user(self):
        u = User.objects.create_superuser(email='f@f.com', password='abc')
        assert u.is_active is True
        assert u.is_staff is True
        assert u.is_superuser is True

        assert u.email == 'f@f.com', "Email field is case sensitive"
        u.email = 'fF.com'
        assert u.email != 'fF.com', "Email field is not validated"
        u.email = 'f@Fcom'
        assert u.email != 'f@Fcom', "Email field is not validated"

        assert str(u) == str(u.id)

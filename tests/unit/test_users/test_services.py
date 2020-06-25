# Standard Library1
import re

# Third Party Stuff
from django.test import TestCase

# milife-back Stuff
from milife_back.users.models import User
from milife_back.users.services import *

class UserServicesTestCase(TestCase):

    def test_get_and_authenticate_user(self):
        user = User.objects.create_user(email='f@F.com', password='abc', first_name="F", last_name='B')
        assert get_and_authenticate_user('f@F.com', 'abc') == user, "pass", "Password authentication is not case-sensitive" 

    def test_create_user_account(self):
        u = create_user_account(email='f@F.com', password='abc', first_name="F", last_name='B', number="9999999999")
        assert u.is_active is True
        assert u.is_staff is False
        assert u.is_superuser is False

        assert u.email == 'f@f.com', "Email field is case sensitive"
        u.email = 'fF.com'
        assert u.email != 'fF.com', "Email field is not validated"
        u.email = 'f@Fcom'
        assert u.email != 'f@Fcom', "Email field is not validated"

        assert u.first_name == "F"
        assert u.last_name == "B"

        assert u.number == "9999999999"
        u.number = "989898989"
        assert len(u.number) == 10, "Number field length is not validated"

        assert u.get_full_name() == 'F B'
        assert u.get_short_name() == 'F'
        assert str(u) == str(u.id)


    def test_invite_user(self):
        u = invite_user(email='f@F.com', first_name="F", last_name='B') # maybe not in use
        assert u.is_active is True
        assert u.is_staff is False
        assert u.is_superuser is False

        assert u.email == 'f@f.com', "Email field is case sensitive"
        u.email = 'fF.com'
        assert u.email != 'fF.com', "Email field is not validated"
        u.email = 'f@Fcom'
        assert u.email != 'f@Fcom', "Email field is not validated"

        assert u.first_name == "F"
        assert u.last_name == "B"
        assert u.get_full_name() == 'F B'
        assert u.get_short_name() == 'F'
        assert str(u) == str(u.id)


    def test_get_user_by_email(self):
        u = create_user_account(email='f@F.com', password='abc', first_name="F", last_name='B', number="9999999999")
        assert get_user_by_email(email='f@F.com') == u

    def test_create_accuniq_id(self):
        assert re.match(r'G M[\*]+', create_accuniq_id("G","M"))
        assert re.match(r'JOHN MEYER[\*]+', create_accuniq_id("John","Meyer"))
        assert len(create_accuniq_id("John","Meyer")) == 20
    
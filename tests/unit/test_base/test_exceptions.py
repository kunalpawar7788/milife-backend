# Standard Library1
import re
import json

# Third Party Stuff
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

# milife-back Stuff
from milife_back.base.exceptions import *


class TestBaseException(TestCase):

    def test_400_bad_request(self):
        detail = 'Unexpected error'
        e = BaseException(detail)
        self.assertEqual(e.status_code, 400)

# Standard Library1
import re
import json

# Third Party Stuff
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

# milife-back Stuff
from milife_back.base.views import *
from milife_back import urls


class TestErrorPages(TestCase):

    def test_error_handlers(self):
        
        factory = RequestFactory()
        request = factory.get('/')
        
        response = server_error(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('500', str(response))
        self.assertIn('HttpResponseServerError', str(response))
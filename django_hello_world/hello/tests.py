from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from middleware_request import GetRequestsToDB
from mock import MagicMock
from models import RequestInfo
from django.conf import settings


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assingment')
        self.assertContains(response, 'Email: admin@example.com')
        self.assertTemplateUsed(response, 'hello/home.html',)

    def test_middleware(self):
        self.gr = GetRequestsToDB()
        self.request = MagicMock()
        self.request.META['REQUEST_METHOD'] = 'GET'
        self.request.path = '/'
        self.assertEqual(self.gr.process_request(self.request), None)
        req_count = RequestInfo.objects.all().count()
        self.assertEqual(req_count, 1)

    def test_context_processor(self):
        response = self.client.get('/')
        self.assertIn('settings', response.context)
        self.assertEquals(
            response.context['settings'].DATABASES, settings.DATABASES)

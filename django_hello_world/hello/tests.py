from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.template import RequestContext

from middleware_request import GetRequestsToDB
from models import RequestInfo

from mock import MagicMock


class HttpTest(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assingment')
        self.assertContains(response, 'Email: admin@example.com')
        self.assertTemplateUsed(response, 'hello/home.html',)

    def test_middleware(self):
        self.gr = GetRequestsToDB()
        self.request = MagicMock()
        self.request.META['REQUEST_METHOD'] = 'GET'
        self.request.path = reverse('home')
        self.assertEqual(self.gr.process_request(self.request), None)
        req_count = RequestInfo.objects.all().count()
        self.assertEqual(req_count, 1)
        c = Client()
        response = c.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assingment')
        self.assertContains(response, reverse('home'))
        self.assertTemplateUsed(response, 'hello/requests.html',)


    def test_context_processor(self):
        f = RequestFactory()
        c = RequestContext(f.request())
        self.assertTrue(c.get('settings') is settings)

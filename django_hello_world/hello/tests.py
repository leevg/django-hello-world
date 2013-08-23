from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assingment')
        self.assertContains(response, 'Email: admin@example.com')
        self.assertTemplateUsed(response, 'hello/home.html',)

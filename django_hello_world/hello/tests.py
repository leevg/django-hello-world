from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.template import RequestContext
from django.template.defaultfilters import escape, date, linebreaks

from middleware_request import GetRequestsToDB
from models import RequestInfo, UserInfo

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


class UserInfoEditTest(TestCase):
    def logout(self):
        self.client.logout()

    def test_login(self):
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        data = UserInfo.objects.get()
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('edit'))
        self.assertContains(response, data.last_name)
        self.assertContains(response, data.date_of_birth)
        self.assertContains(response, data.email)
        self.assertContains(response, data.skype)
        self.assertContains(response, data.jabber)
        self.assertContains(response, escape(data.bio))
        self.assertContains(response, escape(data.other_contacts))

    def test_post(self):
        data = dict()
        data['first_name'] = 'Oleg'
        data['last_name'] = 'Kudriavcev'
        data['date_of_birth'] = '1991-10-28'
        data['email'] = 'leevg@yandex.ru'
        data['jabber'] = 'vioks@khavr.com'
        data['skype'] = 'vitalik_lee'
        data['bio'] = "my name is vova"
        data['other_contacts'] = "kiev, kovalskyj 5, 325r"
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('edit'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserInfo.objects.count(), 1)
        self.assertContains(response, data['first_name'])
        self.assertContains(response, data['last_name'])
        self.assertContains(response, date(data['date_of_birth']))
        self.assertContains(response, data['email'])
        self.assertContains(response, data['jabber'])
        self.assertContains(response, data['skype'])
        self.assertContains(response, escape(data['bio']))
        self.assertContains(response, escape(data['other_contacts']))

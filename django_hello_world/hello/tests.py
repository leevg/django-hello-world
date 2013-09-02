from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.template import RequestContext, Template, Context
from django.template.defaultfilters import escape, date

from middleware_request import GetRequestsToDB
from models import RequestInfo, UserInfo, ModelLog
from templatetags.hello_tags import edit_tag

from mock import MagicMock

from StringIO import StringIO


class HttpTest(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assingment')
        self.assertContains(response, 'Email: admin@example.com')
        self.assertTemplateUsed(response, 'hello/home.html',)

    def test_middleware(self):
        self.client.get(reverse('home'))
        self.client.get(reverse('requests'))
        req_count = RequestInfo.objects.all().count()
        req = RequestInfo.objects.get(pk=1)
        self.assertEqual(req_count, 1)
        self.assertEqual(req.path, reverse('home'))
        self.assertEqual(req.method, 'GET')
        response = self.client.get(reverse('requests'))
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

    def test_ajax_form(self):
        data = dict()
        data['first_name'] = 'Oleg'
        data['last_name'] = 'Ivanov'
        data['date_of_birth'] = '1991-10-28'
        data['email'] = 'leevg@khavr.com'
        data['jabber'] = 'vioks@khavr.com'
        data['skype'] = 'vitalik_lee'
        data['bio'] = "i was born in 1991"
        data['other_contacts'] = "kiev, kovalskyj 5, 325r"
        self.client.login(username='admin', password='admin')
        self.client.post(reverse('edit'), data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(UserInfo.objects.count(), 1)

        userinfo = UserInfo.objects.get(pk=1)

        for key, value in data.items():
            if key != 'date_of_birth':
                self.assertEqual(getattr(userinfo, key), value)


class EditLinkTest(TestCase):
    def test_edit_tag(self):
        userinfo = UserInfo.objects.get(pk=1)
        self.assertEqual(edit_tag(userinfo), '/admin/hello/userinfo/1/')

    def test_edit_tag_in_context(self):
        rendered = Template(
            '{% load hello_tags %}'
            '{% edit_tag object %}'
        ).render(Context({'object': UserInfo.objects.get(pk=1)}))

        self.assertTrue('admin/hello/userinfo/1/' in rendered)


class CommandTest(TestCase):
    def check_output(self, output):
        for model_type in ContentType.objects.all():
            self.assertIn('%s_%s - %d' % (
                model_type.app_label,
                model_type.model,
                model_type.model_class().objects.count()),
                output
            )

    def test_all_models_command(self):
        stdout = StringIO()
        stderr = StringIO()
        call_command('print_models', stderr=stderr, stdout=stdout)
        self.check_output(stdout.getvalue())

    def check_last_log_entry_for_action(self, model, action):
        log = ModelLog.objects.order_by('-created_at')
        self.assertTrue(len(log) > 0)
        log_entry = log[0]
        self.assertEquals(log_entry.app_label, model._meta.app_label)
        self.assertEquals(log_entry.model_name, model.__class__.__name__)
        self.assertEquals(log_entry.action, action)

    def test_model_log(self):
        userinfo = UserInfo.objects.get(pk=1)
        userinfo.last_name = 'last_name changed'
        userinfo.save()
        self.check_last_log_entry_for_action(userinfo, ModelLog.ACTION_UPDATE)

        request = RequestInfo(path='/hello/hello', method='GET')
        request.save()
        self.check_last_log_entry_for_action(request, ModelLog.ACTION_CREATE)
        request.delete()
        self.check_last_log_entry_for_action(request, ModelLog.ACTION_DELETE)


class PriorityTest(TestCase):
    def setUp(self):
        RequestInfo.objects.all().delete()

    def tearDown(self):
        RequestInfo.objects.all().delete()

    def test_default_priority(self):
        self.client.get('/')
        entry = RequestInfo.objects.get(pk=1)
        self.assertEqual(entry.priority, 1)

    def test_priority_ordering(self):
        for i in range(20):
            self.client.get(reverse('home'))
        self.client.get(reverse('edit'))
        entry = RequestInfo.objects.latest('time')
        entry.priority = 10
        entry.save()
        response = self.client.get(reverse('requests'))
        self.assertContains(response, reverse('edit'))

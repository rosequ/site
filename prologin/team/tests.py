from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from prologin.tests import Validator
from team.models import Role, TeamMember


class TeamTest(TestCase):
    def setUp(self):
        self.validator = Validator()
        self.client = Client()
        u = User.objects.create_user('jm', 'joseph.marchand@prologin.org', 'joseph-password')
        r = Role(name="test role", rank=3)
        r.save()
        t = TeamMember(year=2013, role=r, user=u)
        t.save()

    def test_http_response(self):
        """
        Tests the HTTP response.
        """
        response = self.client.get(reverse('team:year', args=(13,)))
        self.assertEqual(response.status_code, 404, 'invalid HTTP status code for team:year')

        response = self.client.get(reverse('team:year', args=(2013,)))
        self.assertEqual(response.status_code, 200, 'invalid HTTP status code for team:year')

    def test_html(self):
        """
        Tests the HTML's compliance with the W3C standards.
        """
        response = self.client.get(reverse('team:year', args=(2013,)))
        valid = self.validator.checkHTML(response.content)
        self.assertEqual(valid, True, 'invalid HTML for team:year')

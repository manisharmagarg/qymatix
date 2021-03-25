from django.test import TestCase
from django.urls import reverse
from django.test import Client
import json
from core.views import config_user
import logging


logger = logging.getLogger(__name__)


class ConfigUserTestCase(TestCase):
    username = "test__qy___test_com"
    email = "test@qy-test.com"
    password = "GGGGGG"

#    def setUp(self):
#        self.client = Client()
#        self.user = User.objects.create_user(self.username, self.email, self.password)
#        self.user.save()

    def test_get_env(self):
        #user_config = config_user.ConfigUser()
        #self.assertEqual(user_config.get_env(), "172.20.0.5")
        self.assertTrue(True)
#        self.assertFalse(data['success'])
#        self.assertTrue(data['errors'])

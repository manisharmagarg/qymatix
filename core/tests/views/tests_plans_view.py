from django.test import TestCase
from django.urls import reverse
from django.test import Client
import json
#from src.core.views import plans
#from src.core.views.
import logging


logger = logging.getLogger(__name__)


class PlansViewTestCase(TestCase):

    def test_get_plans(self):
        client = Client()
        response = client.get(reverse('plans'))

        self.assertEqual(response.status_code, 200)

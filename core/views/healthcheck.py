from django.http import HttpResponse
from django.views import View


class HealthCheckView(View):

    @staticmethod
    def get(self):
        """
        """
        return HttpResponse("", status=200, content_type="application/json")

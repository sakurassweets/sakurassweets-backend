from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import Test


class Home(APIView):

    def get(self, request):
        data = Test.objects.get(pk=1)
        return Response({"message": data.title})

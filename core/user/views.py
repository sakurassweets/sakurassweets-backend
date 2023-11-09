from rest_framework.views import APIView
from rest_framework.response import Response


class Test(APIView):

    def get(self, request):
        return Response({"message": "Message from Backend"})

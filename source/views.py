from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.api.serializers import get_answer


@api_view(['GET'])
def ping_view(request: Request) -> Response:
    answer = get_answer(account=None, operation='ping')
    return Response(answer, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import (AccountOperationSerializer, AccountStatusSerializer,
                          get_answer)
from ..services import AccountBusinessLogic


@api_view(['POST'])
def add_view(request: Request) -> Response:
    data = request.data
    serializer = AccountOperationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    business_logic = AccountBusinessLogic(
        serializer.validated_data['account'].uuid)
    account = business_logic.add(serializer.validated_data['amount'])
    answer = get_answer(
        account, 'add', **{'add_amount': serializer.validated_data['amount']})
    return Response(data=answer, status=status.HTTP_200_OK)


@api_view(['POST'])
def substract_view(request: Request) -> Response:
    data = request.data
    serializer = AccountOperationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    business_logic = AccountBusinessLogic(
        serializer.validated_data['account'].uuid)
    account = business_logic.substract(serializer.validated_data['amount'])
    answer = get_answer(
        account, 'substract',
        **{'substract_amount': serializer.validated_data['amount']})
    return Response(data=answer, status=status.HTTP_200_OK)


@api_view(['GET'])
def status_view(request: Request) -> Response:
    data = request.query_params
    serializer = AccountStatusSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    account = serializer.validated_data['account']
    answer = get_answer(account, 'status')
    return Response(data=answer, status=status.HTTP_200_OK)

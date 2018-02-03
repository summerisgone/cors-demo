from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wallet, Transfer
from .serializers import WalletSerializer, TransferSerializer, TransferModelSerializer


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication, )
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def tx(request):
    serializer = TransferSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.data['user_to'] == request.user.username:
            return Response({'errors': [
                {'wallet_to': 'Can not transfer to yourself'}
            ]}, status=status.HTTP_400_BAD_REQUEST)
        transfer = Transfer(
            amount=serializer.data['amount'],
            wallet_to=Wallet.objects.get(user__username=serializer.data['user_to']),
            wallet_from=Wallet.objects.get(user__id=request.user.pk)
        )
        transfer.full_clean()
        transfer.save()
        return Response({'status': 'ok'})
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@xframe_options_exempt
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def token(request):
    if request.GET['origin'] in settings.CORS_ORIGIN_WHITELIST:
        try:
            auth_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            auth_token = Token.objects.create(user=request.user)
        return Response(dict(token=auth_token.key))
    else:
        return Response(dict(error='origin not supported'), status=status.HTTP_400_BAD_REQUEST)

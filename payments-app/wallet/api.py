from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import list_route, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WalletSerializer, TransferSerializer, TransferModelSerializer
from .models import Wallet, Transfer


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication, )
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)


class TransferModelViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransferModelSerializer

    def get_queryset(self):
        current_wallet = self.request.user.wallet.get()
        return Transfer.objects.filter(
            Q(wallet_from=current_wallet) | Q(wallet_to=current_wallet)
        ).order_by('-timestamp')


@api_view(['POST'])
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

from django.db.models import Q
from rest_framework import viewsets
from .serializers import WalletSerializer, TransferSerializer
from .models import Wallet, Transfer


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WalletSerializer

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)


class TransferViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransferSerializer

    def get_queryset(self):
        current_wallet = self.request.user.wallet.get()
        return Transfer.objects.filter(
            Q(wallet_from=current_wallet) | Q(wallet_to=current_wallet)
        ).order_by('-timestamp')

from rest_framework import serializers
from .models import Wallet, Transfer


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance', 'user')


class TransferModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class TransferSerializer(serializers.Serializer):
    user_to = serializers.CharField(required=True, allow_blank=False, max_length=100)
    amount = serializers.DecimalField(required=True, decimal_places=2, max_digits=19)

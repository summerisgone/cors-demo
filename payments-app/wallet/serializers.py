from rest_framework import serializers
from .models import Wallet, Transfer


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance', 'user')


class TransferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

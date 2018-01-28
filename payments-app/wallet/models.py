from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save


class Wallet(models.Model):
    balance = models.DecimalField('Balance', decimal_places=2, max_digits=19)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='wallet')

    def __str__(self):
        return self.user.username


class Transfer(models.Model):
    amount = models.DecimalField('Balance', decimal_places=2, max_digits=19)
    wallet_from = models.ForeignKey('wallet.Wallet', on_delete=models.CASCADE, related_name='wallet_from')
    wallet_to = models.ForeignKey('wallet.Wallet', on_delete=models.CASCADE, related_name='wallet_to')
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.wallet_from.id == self.wallet_to.id:
            raise ValidationError('Can not transfer to yourself')
        if self.wallet_from.balance < self.amount:
            raise ValidationError('Not enough funds to transfer')


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        wallet = Wallet(user=user, balance=Decimal('100.0'))
        wallet.save()

post_save.connect(create_profile, sender='auth.User')


def transfer_sync(sender, **kwargs):
    transfer = kwargs['instance']
    if kwargs['created']:
        transfer.wallet_to.balance = transfer.wallet_to.balance + transfer.amount
        transfer.wallet_from.balance = transfer.wallet_from.balance - transfer.amount
        transfer.wallet_to.save()
        transfer.wallet_from.save()

post_save.connect(transfer_sync, sender='wallet.Transfer')

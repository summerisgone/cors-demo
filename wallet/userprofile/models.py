from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    balance = models.DecimalField('Balance', decimal_places=2, max_digits=19)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username


class Transfer(models.Model):
    amount = models.DecimalField('Balance', decimal_places=2, max_digits=19)
    profile_from = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile_from')
    profile_to = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile_to')
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        print('transfer clean')
        if self.profile_from.id == self.profile_to.id:
            raise ValidationError('Can not transfer to yourself')
        if self.profile_from.balance < self.amount:
            raise ValidationError('Not enough funds to transfer')


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user, balance=Decimal('100.0'))
        profile.save()

post_save.connect(create_profile, sender='auth.User')


def transfer_sync(sender, **kwargs):
    transfer = kwargs['instance']
    if kwargs['created']:
        profile_from = transfer.profile_from
        profile_to = transfer.profile_to
        profile_from.balance = profile_from.balance - transfer.amount
        profile_to.balance = profile_to.balance + transfer.amount
        profile_from.save()
        profile_to.save()

post_save.connect(transfer_sync, sender='userprofile.Transfer')

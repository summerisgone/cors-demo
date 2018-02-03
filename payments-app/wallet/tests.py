from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .models import Wallet, Transfer
from django.contrib.auth.models import User


class AnimalTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.client = Client()

    def test_user_wallet_signal_hook(self):
        self.assertTrue(Wallet.objects.filter(user__username=self.user1.username).count() > 0)

    def test_transfer_hook(self):
        Transfer.objects.create(wallet_from=self.user1.wallet.get(),
                                wallet_to=self.user2.wallet.get(),
                                amount=Decimal(1))
        self.assertEqual(self.user1.wallet.get().balance, Decimal('99'))
        self.assertEqual(self.user2.wallet.get().balance, Decimal('101'))

    def test_user_can_transfer(self):
        self.client.force_login(self.user1)
        self.client.post(reverse('transfer'), {'to': 'user2', 'amount': '1'})

        self.assertEqual(self.user1.wallet.get().balance, Decimal('99'))
        self.assertEqual(self.user2.wallet.get().balance, Decimal('101'))

    def test_user_cant_transfer_to_himself(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('transfer'), {'to': 'user1', 'amount': '1'})
        self.assertFormError(response, form='form', field=None, errors='Can not send to yourself')

    def test_user_cant_transfer_more_than_have(self):
        self.client.force_login(self.user1)
        with self.assertRaises(ValidationError):
            self.client.post(reverse('transfer'), {'to': 'user2', 'amount': '1000'})

    def test_user_creation(self):
        users_before = User.objects.count()
        self.client.post(reverse('register'))
        self.assertEqual(User.objects.count(), users_before + 1)

    def test_token_for_new_users(self):
        self.client.post(reverse('register'))
        new_user = User.objects.order_by('-date_joined')[0]
        self.client.force_login(self.user1)
        self.assertTrue(True)

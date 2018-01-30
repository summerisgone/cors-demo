from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import TransferForm
from django.urls import reverse

from .models import Wallet, Transfer

@login_required
def balance(request):
    current_wallet = request.user.wallet.get()
    profile = Wallet.objects.get(user_id=request.user.pk)
    transfers = Transfer.objects.filter(
        Q(wallet_from=current_wallet) | Q(wallet_to=current_wallet)
    ).order_by('-timestamp')[:10]
    return render(request, 'wallet/balance.html', {
        'user': request.user,
        'balance': profile.balance,
        'transfers': transfers,
        'current_wallet': current_wallet
    })

@login_required
def send_money(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        form.current_user = request.user
        if form.is_valid():
            transfer = Transfer(
                amount=form.cleaned_data['amount'],
                wallet_to=Wallet.objects.get(user__username=form.cleaned_data['to']),
                wallet_from=Wallet.objects.get(user__id=request.user.pk)
            )
            transfer.full_clean()
            transfer.save()
            return HttpResponseRedirect(reverse('balance'))
    else:
        form = TransferForm()
    return render(request, 'wallet/transfer.html', {
        'form': form
    })

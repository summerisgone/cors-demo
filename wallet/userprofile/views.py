from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import TransferForm
from django.urls import reverse

from .models import Profile, Transfer

@login_required
def balance(request):
    current_profile = request.user.profile.get()
    profile = Profile.objects.get(user_id=request.user.pk)
    transfers = Transfer.objects.filter(
        Q(profile_from=current_profile) | Q(profile_to=current_profile)
    ).order_by('-timestamp')[:10]
    return render(request, 'balance.html', {
        'user': request.user,
        'balance': profile.balance,
        'transfers': transfers,
        'current_profile': current_profile
    })

@login_required
def send_money(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        form.current_user = request.user
        if form.is_valid():
            transfer = Transfer(
                amount=form.cleaned_data['amount'],
                profile_to=Profile.objects.get(user__username=form.cleaned_data['to']),
                profile_from=Profile.objects.get(user__id=request.user.pk)
            )
            transfer.full_clean()
            transfer.save()
            return HttpResponseRedirect(reverse('balance'))
    else:
        form = TransferForm()
    return render(request, 'transfer.html', {
        'form': form
    })

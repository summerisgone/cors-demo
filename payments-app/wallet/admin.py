from django.contrib import admin
from .models import Wallet, Transfer


admin.site.register(Wallet)


class TransferAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ['timestamp', 'wallet_to', 'wallet_from', 'amount']

admin.site.register(Transfer, TransferAdmin)

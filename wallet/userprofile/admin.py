from django.contrib import admin
from .models import Profile, Transfer


admin.site.register(Profile)


class TransferAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ['timestamp', 'profile_to', 'profile_from', 'amount']

admin.site.register(Transfer, TransferAdmin)

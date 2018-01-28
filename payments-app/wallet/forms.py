from django import forms
from django.contrib.auth.models import User


class TransferForm(forms.Form):
    amount = forms.DecimalField(label='Amount', required=True)
    to = forms.CharField(label='To', required=True)

    def clean(self):
        cleaned_data = super().clean()
        to = cleaned_data.get('to')
        if User.objects.filter(username=to).none():
            raise forms.ValidationError("Specify existing recepient")
        if to == self.current_user.username:
            raise forms.ValidationError("Can not send to yourself")

# -*- coding: utf8 -*-
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic.base import TemplateView
from .views import balance, send_money

urlpatterns = [
    path('', balance, name='balance'),
    path('send', send_money, name='transfer'),
    path('token', xframe_options_exempt(login_required(
        TemplateView.as_view(template_name='wallet/token_iframe.html')
    )), name='token'),
]

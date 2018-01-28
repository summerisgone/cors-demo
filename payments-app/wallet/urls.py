# -*- coding: utf8 -*-
from django.urls import path
from .views import balance, send_money

urlpatterns = [
    path('', balance, name='balance'),
    path('send', send_money, name='transfer'),
]

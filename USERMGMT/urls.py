#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from USERMGMT.views import *


urlpatterns = patterns('',
    url(r'login/$', connect, name='connect'),
    url(r'logout/$', killUser, name='killUser'),
    url(r'abonnement/$', ask_abo, name='ask_abo'),
    url(r'display/$', showUser, name='showUser'),
    url(r'modification/$', changeUser, name='changeUser'),
    url(r'newPassword/$', newPassword, name='newPassword'),
    url(r'forgottenPassword/$', forgottenPassword, name='forgottenPassword'),
)
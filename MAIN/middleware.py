#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404

from mezzanine.conf import settings
from models import *

class AuthXMiddleware(object):
    def process_request(self,request):
        # forbidden_domain = "lalettre"
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/user/login?next='+request.path)
        else:
            print "request.user.is_authenticated = {}".format(request.user.is_authenticated())
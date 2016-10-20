#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils.http import base36_to_int
from django.core.mail import send_mail

from .models import Client
User = get_user_model()

from webservices import *

import uuid



class ClientAuthBackend(ModelBackend):

    def authenticate(self, **kwargs):
        if kwargs:
            username = kwargs.pop("username", None)
            if username:
                username_or_email = (Q(username=username) | Q(email=username)) & Q(is_staff=True)
                password = kwargs.pop("password", None)
                try:
                    user = User.objects.get(username_or_email, **kwargs)
                except User.DoesNotExist:
                    # Delegation of webservices.authenticateByEmail to LoginForm.is_valid()
                    codeClient = ABM_ACCES_CLIENT(username,password)

                    # fetch "getAbonnements"
                    xml = getAbonnements(codeClient)
                    aboList = repr(xml)
                    active_abo = False
                    for abonnement in xml.children().children().children():
                        if int(abonnement.refTitre) == 26 and str(abonnement.obsolete) == 'false':
                            active_abo = True

                    # Green light from aboWeb
                    if active_abo:
                        print "ALL LIGHTS ARE GREEN"
                        username_or_email = Q(username=username) | Q(email=username)
                        try:
                            user = User.objects.get(username_or_email, **kwargs)
                            return user
                        except User.DoesNotExist:
                            print "creating local user"
                            userId = int(codeClient)
                            try:
                                k = User.objects.get(username=userId)
                            except User.DoesNotExist:
                                print 'User %s DoesNotExist' % codeClient
                                k = User.objects.create_user(username=userId, email=username, password=make_password(password))
                                k.save()
                                try:
                                    send_mail('Creation de compte utilisateur - pnpapetier.com', 
                                        """ Une réplique de l'utilisateur {} vient d'être créée sur la base locale de pnpapetier.com sous l'(U.U)I.D. {}""".format(username,userId),
                                        'n.burton@groupembc.com', 
                                        ['philippe@lesidecar.fr',],
                                        fail_silently=False)
                                    print "MAIL HAS BEEN SENT !"
                                except 'SMTPConnectError' as e:
                                    pass
                            return k
                    # RED FLAG
                    else:
                        # Shoot mail to rebuy
                        print 'OBSOLETE'
                        pass
                else:
                    if user.check_password(password):
                        return user
            else:
                if 'uidb36' not in kwargs:
                    return
                kwargs["id"] = base36_to_int(kwargs.pop("uidb36"))
                token = kwargs.pop("token")
                try:
                    user = User.objects.get(**kwargs)
                except User.DoesNotExist:
                    pass
                else:
                    if default_token_generator.check_token(user, token):
                        return user

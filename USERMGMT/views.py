#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from random import randint

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate, get_backends, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives

from mezzanine.utils.urls import login_redirect, next_url
from forms import *

from MAIN.webservices import *

get_backends()

def connect(request):
    error = False
    if request.GET:
        articleAttempt = True
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return login_redirect(request)
            else:
                obsolete = True
                return render(request, 'login.html', locals())
    else:
        form = LoginForm()
    return render(request, 'login.html', locals())

def killUser(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def showUser(request):
    display = True
    if request.POST:
        form = UserModifForm(request.POST)
        if form.is_valid:
            print "ok"
    else:
        form = UserModifForm()
    return render(request, 'login.html', locals())

@login_required
def changeUser(request):
    modification = True
    if request.POST:
        currentForm = False
        if 'modification_mail' in request.POST:
            print "MODIF MAIL"
            currentForm = MailModifForm
        elif 'confirmation_mail' in request.POST:
            print "CONFIRMATION MAIL"
            currentForm = MailConfirmationForm
        elif 'modification_password' in request.POST:
            print "MODIF PASSWORD"
            currentForm = PasswordModifForm
        else:
            raise ValueError('request.POST dict does not contain the required values')
        form = currentForm(request.POST)
        if form.is_valid():
            # proceed to changes accordingly w/ type(form)
            user = getClient(request.user.username)
            if currentForm == MailModifForm:
                try:
                    confirmation_mail = form.cleaned_data['mail']
                    message = 'Un email a été envoyé à %s contenant un code de confirmation.' % form.cleaned_data['mail']
                    form3 = MailConfirmationForm(initial={'confirmation_mail': confirmation_mail})
                except:
                    error = "Une erreur est survenue."
                    form1 = MailModifForm(request.POST)
                    form2 = PasswordModifForm()
            elif currentForm == MailConfirmationForm:
                try:
                    user.email = request.POST['confirmation_mail']
                    createOrUpdateClientEx(user)
                    user = User.objects.get(username=request.user.username)
                    user.email = request.POST['confirmation_mail']
                    user.save()
                    message = "Votre nouvelle adresse mail a bien été enregistrée."
                except:
                    confirmation_mail = True
                    error = "Une erreur est survenue."
                    raise IOError('Une erreur est survenue lors de la confirmation de la nouvelle adresse mail.')
            elif currentForm == PasswordModifForm:
                try:
                    newPassWord = form.cleaned_data['password1']
                    user.motPasseAbm = newPassWord
                    createOrUpdateClientEx(user)
                    message = 'Mot de passe modifié avec succès.'
                    try:
                        subject= 'MODIFICATION MOT DE PASSE - pnpapetier.com'
                        from_email= settings.ADMINS[1][1]
                        to = str(user.email)
                        text_content = "Votre nouveau mot de passe est: " + newPassWord
                        html_content = "<p> Votre nouveau mot de passe est le suivant : <br/> <b>" + newPassWord + "</b> </p>"
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except:
                        print "ERROR WHILE SENDING MAIL"
                        pass
                except:
                    raise IOError('ABMuser.motPasseAbm update has failed')
            form1 = MailModifForm()
            form2 = PasswordModifForm()
        else:
            # Form is not valid()
            if currentForm == MailModifForm:
                form1 = MailModifForm(request.POST)
                form2 = PasswordModifForm()
            elif currentForm == PasswordModifForm:
                form1 = MailModifForm()
                form2 = PasswordModifForm(request.POST)
            else:
                confirmation_mail = True
                form3 = MailConfirmationForm(request.POST)
    else:
        form1 = MailModifForm()
        form2 = PasswordModifForm()
    return render(request, 'modificationUser.html', locals())

@login_required
def newPassword(request):
    formTitle = 'Réinitialisez votre mot de passe.'
    if request.POST:
        form = OnlyEmailForm(request.POST)
        if form.is_valid():
            user = getClient(request.user.username)
            try:
                newPassword = b64encode(sha1(str(randint(73,1073))).digest())[:6]
                subject= 'REINITIALISATION Mot de Passe - pnpapetier.com'
                from_email= settings.ADMINS[1][1]
                to = str(user.email)
                text_content = "Votre nouveau mot de passe est: " + newPassword + ". Nous vous recommandons de changer ce dernier dans l'espace utilisateur de pnpapetier.com. "
                html_content = "<p> Votre nouveau mot de passe est le suivant : <br/> <b>" + newPassword + "</b> </p> <p>Nous vous recommandons de changer ce dernier dans votre espace utilisateur, sur pnpapetier.com</p>"
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                user.motPasseAbm = newPassword
                createOrUpdateClientEx(user)
            except ValueError:
                print 'FAILURE'
                pass
    else:
        form = OnlyEmailForm()
    return render(request,'changePassword.html', locals())

def forgottenPassword(request):
    """ No login_required
        (Non-Authenticated) user must enter a valid email which will receive its current Password
    """
    formTitle = 'Récupérez votre mot de passe'
    if request.POST:
        form = OnlyEmailForm(request.POST)
        if form.is_valid():
            send_mail = ABM_MOT_PASSE_OUBLIE(request.POST['mail'])
            if str(send_mail) == "01":
                goToLogin = True
                return render(request,'changePassword.html', locals())
            else:
                error = "Aucun email n'a pu être envoyé à l'adresse email soumise."
            return render(request,'changePassword.html', locals())
        else:
            form = OnlyEmailForm(request.POST)
            return render(request,'changePassword.html', locals())
    else:
        form = OnlyEmailForm()
        return render(request,'changePassword.html', locals())


def ask_abo(request):
    if request.POST:
        form = AskAboForm(request.POST)
        if form.is_valid():
            subject= "DEMANDE ABONNEMENT - "+ request.POST['revue']
            from_email= settings.ADMINS[1][1]
            to = "abonnement@groupembc.com"
            text_content = "Une nouvelle demande d'abonnement vient d'être soumise sur pnpapetier.com pour le(s) magazine(s) : "+ request.POST['revue'] +". Les informations sont les suivantes : "+ request.POST['gender'] +" (prénom) "+ request.POST['prenom']+" (nom)"+ request.POST['nom'] +" (société)"+ request.POST['societe'] +". Email = "+ request.POST['email'] + ". Tel: "+ request.POST['phone']
            html_content = "<p>Une nouvelle demande d'abonnement vient d'être soumise sur pnpapetier.com pour le(s) magazine(s) : "+ request.POST['revue'] +".</p> <p>Les informations sont les suivantes : </p> genre = "+ request.POST['gender'] +"<br /> prénom = "+ request.POST['prenom']+"<br /> nom = "+ request.POST['nom'] +"<br /> société = "+ request.POST['societe'] +" <br /> Email = "+ request.POST['email'] + "<br /> Tel: "+ request.POST['phone']
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            message = "Votre demande a bien été prise en compte. Un conseiller du groupe MBC vous contactera dans les plus brefs délais."
        else:
            form = AskAboForm(request.POST)
            # error = "Données soumises invalides..."
    else:
        form = AskAboForm()
    return render(request, 'abonnement.html', locals())


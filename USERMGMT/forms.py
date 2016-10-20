#-*- coding: utf-8 -*-
from time import strftime

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives

from base64 import b64encode
from hashlib import sha1

from MAIN.webservices import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Adresse mail', widget=forms.EmailInput)
    password = forms.CharField(label='mot de passe', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if str(ABM_TEST_MAIL(username)) != '00':
            msg=''
            self.add_error('username', msg)
            self.add_error('password', msg)
            raise forms.ValidationError("Adresse email inexistante.")
        aboAuthResult = authenticateByEmail(username,password)
        if aboAuthResult != 'true':
            msg = ''
            self.add_error('password', msg)
            raise forms.ValidationError("Mot de passe incorrect.")
        return self.cleaned_data

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password',]


class MailModifForm(forms.Form):
    mail = forms.CharField(label='Adresse mail', widget=forms.EmailInput)

    def clean(self):
        # TODO -> ovveride mail regex (No default ".tld" verification)
        mail = self.cleaned_data.get('mail')
        mailExist = ABM_TEST_MAIL(mail)
        mailExist = str(mailExist)
        if mailExist == '00':
            msg='adresse mail invalide'
            self.add_error('mail', msg)
            raise forms.ValidationError("Adresse mail déjà présente en base de données.")
        elif mailExist != '01':
            msg='Adresse mail rejetée'
            self.add_error('mail', msg)
            raise forms.ValidationError("ABM_TEST_MAIL return failed")
        try:
            subject= 'MODIFICATION ADRESSE MAIL - pnpapetier.com'
            from_email=settings.ADMINS[0][1]
            toHash = str(mail) + strftime("%d/%m/%Y")
            text_content = "Veuillez trouver ci-après le code de vérification pour changer votre adresse mail: " + b64encode(sha1(toHash).digest())[:6]
            html_content = "<p>Veuillez trouver ci-après le code de vérification pour changer votre adresse mail: <br/> <b>" + b64encode(sha1(toHash).digest())[:6] + "</b> </p>"
            msg = EmailMultiAlternatives(subject, text_content, from_email, [mail])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            msg = ""
            self.add_error('mail', msg)
            raise forms.ValidationError("L'envoi d'email à l'adresse %s a échoué." % str(mail))
        return self.cleaned_data

class MailConfirmationForm(forms.Form):
    code_verification = forms.CharField(max_length=255, help_text='Entrez le code de vérification qui vous a été envoyé sur l\'adresse mail renseignée à l\'étape précédente.')
    confirmation_mail = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        code = self.cleaned_data.get('code_verification')
        mail = self.cleaned_data.get('confirmation_mail')
        if not b64encode(sha1(mail+strftime('%d/%m/%Y')).digest())[:6] == code:
            msg=''
            self.add_error('code_verification', msg)
            raise forms.ValidationError("Code de vérification incorrect.")
        return self.cleaned_data


class PasswordModifForm(forms.Form):
    password1 = forms.CharField(label='mot de passe', help_text='6 caractères minimum', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirmation', help_text='Entrez le même mot de passe qu\'au dessus', widget=forms.PasswordInput)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            msg=''
            self.add_error('password1', msg)
            self.add_error('password2', msg)
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        elif len(password1) < 6:
            msg=''
            self.add_error('password1', msg)
            self.add_error('password2', msg)
            raise forms.ValidationError("Mot de passe trop court. Veuillez entrer un mot de passe d'au moins 6 caractères")
        return self.cleaned_data


class OnlyEmailForm(forms.Form):
    mail = forms.CharField(label='Adresse mail', widget=forms.EmailInput)

    def clean(self):
        mail = self.cleaned_data.get('mail')
        mailExist = ABM_TEST_MAIL(mail)
        mailExist = str(mailExist)
        if mailExist != '00':
            msg='Adresse mail inconnue.'
            self.add_error('mail', msg)
            raise forms.ValidationError("L'adresse mail doit être associée à un compte existant.")
        return self.cleaned_data


class AskAboForm(forms.Form):
    GENDER_CHOICES = (
        ('M.', 'Monsieur'),
        ('Mme', 'Madame'),
        ('Mlle', 'Mademoiselle'),
    )
    gender = forms.ChoiceField(label="intitulé",choices=GENDER_CHOICES)
    nom = forms.CharField(label='Nom', max_length=100, required=True)
    prenom = forms.CharField(label='Prénom', max_length=50, required=True)
    email = forms.EmailField(label="Adresse e-mail",required=True)
    societe= forms.CharField(label='Société', max_length=50, required=True)
    phone = forms.CharField(label='Téléphone',required=False)
    REVUE_CHOICES = (
        ('PNP', 'PNP'),
        ('La Lettre PNP', 'La Lettre PNP'),
        ('PNP + La Lettre PNP', 'PNP + La Lettre PNP'),
    )
    revue = forms.ChoiceField(choices=REVUE_CHOICES)

    def clean(self):
        email = self.cleaned_data.get('email')
        gender = self.cleaned_data.get('gender')
        nom = self.cleaned_data.get('nom')
        revue = self.cleaned_data.get('revue')
        phone = self.cleaned_data.get('phone')
        if phone == "":
            msg='Merci de remplir votre numéro de téléphone afin que nous puissions vous contacter pour finaliser votre abonnement.'
            self.add_error('phone', msg)
            raise forms.ValidationError("Veuillez indiquer un numéro de téléphone valide. ")
        try:
            subject= "Votre demande abonnement a bien été prise en compte"
            from_email = settings.ADMINS[1][1]
            to = email
            text_content = "Bonjour "+ str(gender) +" "+ str(nom) +". Votre demande d’abonnement à "+ str(revue) + "a bien été prise en compte. Notre service abonnement va prendre contact avec vous très rapidement afin de finaliser votre demande. D’ici là, pour toutes questions, vous pouvez nous joindre aux coordonnées suivantes : ELTA - Service Abonnement ,20 place de l’Horloge,84 000 Avignon,Mail : abonnement@groupembc.com,Tel : 04 90 14 61 41.   Cordialement, Le service abonnement. "
            html_content = "<p>Bonjour "+ str(gender) +" "+ str(nom) +"</p><p>Votre demande d’abonnement à <strong>"+ str(revue) +"</strong> a bien été prise en compte.</p> <p>Notre service abonnement va prendre contact avec vous très rapidement afin de finaliser votre demande. </p><p>D’ici là, pour toutes questions, vous pouvez nous joindre aux coordonnées suivantes : </p><p>ELTA - Service Abonnement <br />20 place de l’Horloge <br />84 000 Avignon <br />Mail : abonnement@groupembc.com <br />Tel : 04 90 14 61 41 <br /></p>Cordialement, <br />Le service abonnement."
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            self.add_error('email', '')
            raise forms.ValidationError("L'adresse mail soumise semble invalide")
        return self.cleaned_data




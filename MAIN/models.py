#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.sites.models import *
from django.utils.translation import ugettext, ugettext_lazy as _

from settings import MEDIA_ROOT
from mezzanine.pages.models import Page
from mezzanine.core.models import RichText
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.utils.models import upload_to


class Product(Page, RichText):
    illustration = FileField(verbose_name=_("illustration"),
        upload_to=upload_to("MAIN.Product.illustration", "product"),
        format="Image", max_length=255, null=True, blank=True)

    def __unicode__(self):
        if self.parent and self.parent.title != 'PRODUITS':
            return '%s [sous-catégorie de produit de: %s]' % (self.title.upper(), self.parent.title)
        else:
            return '%s' % (self.title.upper())

    class Meta:
        verbose_name='PRODUIT'
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.in_menus = []
        if not self.parent:
            self.parent = Page.objects.get(title='PRODUITS')
        super(Product, self).save(*args, **kwargs)

class Brand(Page, RichText):
    products = models.ManyToManyField('Product',blank=True)
    topics = models.ManyToManyField('Topic',blank=True)
    illustration = FileField(verbose_name=_("illustration"),
        upload_to=upload_to("MAIN.Brand.illustration", "brand"),
        format="Image", max_length=255, null=True, blank=True)

    def __unicode__(self):
        motherCompany = Company.objects.filter(brands=self)
        companies_str = ''
        if motherCompany:
            for X in motherCompany:
                companies_str += X.title + ', '
        products = Product.objects.filter(brand=self)
        product_str = ''
        if products:
            for product in products:
                product_str +=  product.title + ', '
        return '%s | %s | %s' % (self.title.upper(), companies_str.lower(),  product_str.lower())

    class Meta:
        verbose_name='MARQUE'
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.in_menus = []
        if not self.parent:
            self.parent = Page.objects.get(title='MARQUES')
        super(Brand, self).save(*args, **kwargs)

class Topic(Page, RichText):
    illustration = FileField(verbose_name=_("illustration"),
        upload_to=upload_to("MAIN.Topic.illustration", "topic"),
        format="Image", max_length=255, null=True, blank=True)

    def __unicode__(self):
        if self.parent and self.parent.title != 'RUBRIQUES':
            return '%s [sous-rubrique de: %s]' % (self.title.upper(), self.parent.title)
        else:
            return '%s' % (self.title.upper())

    class Meta:
        verbose_name='RUBRIQUE'
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.in_menus = []
        if not self.parent:
            self.parent = Page.objects.get(title='RUBRIQUES')
        super(Topic, self).save(*args, **kwargs)

class Company(Page, RichText):
    subsidiaries = models.ManyToManyField("self",through='Subsidiary',symmetrical=False)
    illustration = FileField(verbose_name=_("illustration"),
        upload_to=upload_to("MAIN.Company.illustration", "company"),
        format="Image", max_length=255, null=True, blank=True)
    topics = models.ManyToManyField('Topic',blank=True)
    brands = models.ManyToManyField('Brand',blank=True)
    adress = models.CharField(max_length=255, null=False,blank=True)
    zipCode = models.CharField(max_length=255, null=False,blank=True)
    bp = models.CharField(max_length=100,null=False,blank=True)
    area = models.CharField(max_length=255, null=False,blank=True)
    city = models.CharField(max_length=255, null=False,blank=True)
    country = models.CharField(max_length=255,null=False,blank=True)
    email = models.TextField(null=False,blank=True)
    tel = models.TextField(null=False,blank=True)
    fax = models.TextField(null=False,blank=True)
    website = models.TextField(null=False,blank=True)
    highlight = models.BooleanField(default=False,null=False,blank=True)

    def __unicode__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name='SOCIETE'
        ordering = ['title']

    def save(self, *args, **kwargs):
        self.in_menus = []
        if not self.parent:
            self.parent = Page.objects.get(title='SOCIETES')
        # if not self.area:
            # if not self.country or self.country.lower() == "france":
                # deduce area from zipCode[:2]
        super(Company, self).save(*args, **kwargs)

class Subsidiary(models.Model):
    top_company = models.ForeignKey(Company,related_name='top_companies')
    sub_company = models.ForeignKey(Company,related_name='sub_companies',verbose_name='Société affiliée')
    relation_choices = (
        ('','---'),
        ('Adhérent', 'Adhérent'),
        ('Membre', 'Membre'),
        ('Antenne', 'Antenne'),
        ('Antenne internationale', 'Antenne internationale'),
        ('Filliale', 'Filliale'),
        ('Agence', 'Agence'),
        ('Fédération régionale', 'Fédération régionale'),
        ('Chambre syndicale', 'Chambre syndicale'),
        ('Délégation', 'Délégation'),
    )
    relation = models.CharField(max_length=255,choices=relation_choices,null=False,blank=True,verbose_name='nature de l\'affiliation')
    relation_alt = models.CharField(max_length=255,null=False,blank=True,verbose_name='nature affiliation alternative')

    class Meta:
        verbose_name='Société affiliée'

class Person(Page, RichText):
    illustration = FileField(verbose_name=_("illustration"),
        upload_to=upload_to("MAIN.Person.illustration", "person"),
        format="Image", max_length=255, null=True, blank=True)
    firstName = models.CharField(max_length=255,null=False,blank=True)
    companies = models.ManyToManyField(Company,through='Job')
    adress = models.CharField(max_length=255, null=False,blank=True)
    zipCode = models.CharField(max_length=255, null=False,blank=True)
    area = models.CharField(max_length=255, null=False,blank=True)
    city = models.CharField(max_length=255, null=False,blank=True)
    country = models.CharField(max_length=255,null=False,blank=True)
    email = models.EmailField(null=False,blank=True)
    tel = models.CharField(max_length=255, null=False,blank=True)
    highlight = models.BooleanField(default=False,null=False,blank=True)

    def __unicode__(self):
        return '%s %s' % (self.title.upper(), self.firstName.lower())

    def save(self, *args, **kwargs):
        self.in_menus = []
        self.parent = Page.objects.get(title='MEMBRES')
        super(Person, self).save(*args,**kwargs)

    class Meta:
        verbose_name='INDIVIDU'
        ordering = ['title']

class Job(models.Model):
    person = models.ForeignKey(Person,verbose_name='Employé')
    company = models.ForeignKey(Company)
    title = models.CharField(max_length=255,null=False,blank=True,verbose_name='intitulé du poste')
    # rank = models.IntegerField(null=True,blank=True)
    since = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True,verbose_name='date d\'entrée en fonction')
    until = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True,verbose_name='date de fin de la fonction')

    class Meta:
        verbose_name='Employé'



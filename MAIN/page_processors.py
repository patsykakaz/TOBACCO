from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from mezzanine.pages.page_processors import processor_for
from mezzanine.blog.models import BlogPost, BlogCategory
from .models import *

from mezzanine.core.request import current_request

@processor_for(Person)
def processor_revue(request, page):
    person = Person.objects.get(pk=page.pk)
    person.jobs = Job.objects.filter(person=person)
    return locals()

@processor_for(Company)
def processor_revue(request, page):
    company = Company.objects.get(pk=page.pk)
    subsidiaries = Subsidiary.objects.filter(top_company=company)
    jobs = Job.objects.filter(company=company)
    return locals()

@processor_for(Brand)
def processor_revue(request, page):
    brand = Brand.objects.get(pk=page.pk)
    twin_brands = Brand.objects.filter(title=brand.title)
    twin_brands = twin_brands.exclude(pk=brand.pk)
    distributors = Company.objects.filter(brands__in=[brand])
    return locals()


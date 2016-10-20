#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from mezzanine import template
from MAIN.models import *
register = template.Library()

@register.filter(name='ExtendCompany')
def ExtendCompany(company, *args):
    html = "<h4 class='text-center' style='color:rgb(174,17,28);'>"+company.title+"</h4>"
    if company.adress: 
        html += " <div><b>Adresse: </b>"+company.adress+"</div>"
    if company.city: 
        html += " <div><b>Ville: </b>"+company.city+"</div>"
    if company.zipCode: 
        html += " <div><b>Code postal: </b>"+company.zipCode+"</div>"
    if company.bp: 
        html += " <div><b>Boite postale: </b>"+company.bp+"</div>"
    if company.country: 
        html += " <div><b>Pays: </b>"+company.country+"</div>"
    if company.email: 
        html += " <div><b>Email: </b>"+company.email+"</div>"
    if company.tel:
        html += "<div><b>Téléphone: </b>"+company.tel+"</div>"
    if company.website:
        html += "<div><b>Téléphone: </b>"+company.website+"</div>"
    if company.tel:
        html += "<div><b>Téléphone: </b>"+company.tel+"</div>"
    return html

@register.filter(name='ExtendFilliale')
def ExtendFilliale(sub, *args):
    company = sub.sub_company
    link = sub.relation
    html = "<h4 class='text-center' style='color:rgb(174,17,28);'>"+company.title+"</h4><h5 class='text-center' style='color:rgb(120,120,140);'>"+link+"</h5>"
    if company.adress: 
        html += " <div><b>Adresse: </b>"+company.adress+"</div>"
    if company.city: 
        html += " <div><b>Ville: </b>"+company.city+"</div>"
    if company.zipCode: 
        html += " <div><b>Code postal: </b>"+company.zipCode+"</div>"
    if company.bp: 
        html += " <div><b>Boite postale: </b>"+company.bp+"</div>"
    if company.country: 
        html += " <div><b>Pays: </b>"+company.country+"</div>"
    if company.email: 
        html += " <div><b>Email: </b>"+company.email+"</div>"
    if company.tel:
        html += "<div><b>Téléphone: </b>"+company.tel+"</div>"
    if company.website:
        html += "<div><b>Téléphone: </b>"+company.website+"</div>"
    if company.tel:
        html += "<div><b>Téléphone: </b>"+company.tel+"</div>"
    return html

@register.filter(name='ExtendPerson')
def ExtendPerson(person, *args):
    html = ""
    if type(person) == Person:
        html += ("<h4 class='text-center' style='color:rgb(174,17,28);'>"+person.firstName + " " + person.title+"</h4>")
    if person.adress:
        html += " <div><b>Adresse: </b>"+person.adress+"</div>"
    if person.city:
        html += " <div><b>Ville: </b>"+person.city+"</div>"
    if person.zipCode:
        html += " <div><b>Code postal: </b>"+person.zipCode+"</div>"
    if person.country:
        html += " <div><b>Pays: </b>"+person.country+"</div>"
    if person.email:
        html += " <div><b>Email: </b>"+person.email+"</div>"
    if person.tel:
        html += "<div><b>Téléphone: </b>"+person.tel+"</div>"
    return html

@register.filter(name='ExtendBrand')
def ExtendBrand(brand, *args):
    html = str(brand.title)
    products = brand.products.all()
    for product in products : 
        html += "<span class='text-muted'>"+product.title+"</span> |"
    # html = html[:len(html-1)]
    return html






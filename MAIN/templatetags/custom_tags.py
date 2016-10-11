#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from mezzanine import template
from MAIN.models import *
register = template.Library()

@register.filter(name='ExtendCompany')
def ExtendCompany(company, *args):
    html = "<h3 class='text-center'>"+company.title+"</h3>"
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
    html = "<h3 class='text-center'>"+company.title+"</h3><h5 class='text-center' style='color:rgb(120,120,140);'>"+link+"</h5>"
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
    toggle = False
    html = ""
    if type(person) == Person:
        html += ("<h3 class='text-center'>"+person.firstName + " " + person.title+"</h3>")
    if person.adress:
        toggle = True
        html += " <div><b>Adresse: </b>"+person.adress+"</div>"
    if person.city:
        toggle = True
        html += " <div><b>Ville: </b>"+person.city+"</div>"
    if person.zipCode:
        toggle = True
        html += " <div><b>Code postal: </b>"+person.zipCode+"</div>"
    if person.country:
        toggle = True
        html += " <div><b>Pays: </b>"+person.country+"</div>"
    if person.email:
        toggle = True
        html += " <div><b>Email: </b>"+person.email+"</div>"
    if person.tel:
        toggle = True
        html += "<div><b>Téléphone: </b>"+person.tel+"</div>"
    if toggle:
        return html
    else:
        return False

@register.filter(name='ExtendBrand')
def ExtendBrand(brand, *args):
    html = ""
    products = brand.products.all()
    for product in products : 
        html += "<span class='text-muted'>"+product.title+"</span> |"
    html = html[:len(html-1)]
    return html






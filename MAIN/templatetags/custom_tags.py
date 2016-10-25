#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from mezzanine import template
from MAIN.models import *
register = template.Library()

@register.filter(name='ExtendCompany')
def ExtendCompany(company, *args):
    html = "<h4 class='text-center'>"+company.title+"</h4>"
    if company.adress: 
        html += " <div><b class='text-muted'>Adresse: </b>"+company.adress+"</div>"
    if company.city: 
        html += " <div><b class='text-muted'>Ville: </b>"+company.city+"</div>"
    if company.zipCode: 
        html += " <div><b class='text-muted'>Code postal: </b>"+company.zipCode+"</div>"
    if company.bp: 
        html += " <div><b class='text-muted'>Boite postale: </b>"+company.bp+"</div>"
    if company.country: 
        html += " <div><b class='text-muted'>Pays: </b>"+company.country+"</div>"
    if company.email: 
        html += " <div><b class='text-muted'>Email: </b>"+company.email+"</div>"
    if company.tel:
        html += "<div><b class='text-muted'>Téléphone: </b>"+company.tel+"</div>"
    if company.website:
        html += "<div><b class='text-muted'>Téléphone: </b>"+company.website+"</div>"
    if company.tel:
        html += "<div><b class='text-muted'>Téléphone: </b>"+company.tel+"</div>"
    return html

@register.filter(name='ExtendFilliale')
def ExtendFilliale(sub, *args):
    company = sub.sub_company
    link = sub.relation
    html = "<h4 class='text-center'>"+company.title+"</h4><h5 class='text-center' style='color:rgb(120,120,140);'>"+link+"</h5>"
    if company.adress: 
        html += " <div><b class='text-muted'>Adresse: </b>"+company.adress+"</div>"
    if company.city: 
        html += " <div><b class='text-muted'>Ville: </b>"+company.city+"</div>"
    if company.zipCode: 
        html += " <div><b class='text-muted'>Code postal: </b>"+company.zipCode+"</div>"
    if company.bp: 
        html += " <div><b class='text-muted'>Boite postale: </b>"+company.bp+"</div>"
    if company.country: 
        html += " <div><b class='text-muted'>Pays: </b>"+company.country+"</div>"
    if company.email: 
        html += " <div><b class='text-muted'>Email: </b>"+company.email+"</div>"
    if company.tel:
        html += "<div><b class='text-muted'>Téléphone: </b>"+company.tel+"</div>"
    if company.website:
        html += "<div><b class='text-muted'>Téléphone: </b>"+company.website+"</div>"
    if company.tel:
        html += "<div><b class='text-muted'>Téléphone: </b>"+company.tel+"</div>"
    return html

@register.filter(name='ExtendPerson')
def ExtendPerson(person, *args):
    html = ""
    if type(person) == Person:
        html += ("<h4 class='text-center'>"+person.firstName + " " + person.title+"</h4>")
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
    html = "<h4 class='text-center'>"+brand.title+"</h4>"
    products = brand.products.all()
    if products:
        html += "<span class='text-muted'>Produits distribués : </span>"
        for product in products: 
            html += product.title+" • "
    html = html[:len(html)-2]
    return html






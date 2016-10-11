#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from mezzanine import template
register = template.Library()

@register.filter(name='ExtendCompany')
def ExtendCompany(company, *args):
    try:
        company = Company.objects.get(pk=company.pk)
    except:
        pass
    html = "<div class='text-center'>"+company.title+"</div>"
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



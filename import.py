#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from MAIN.models import *

tree = ET.parse('liste.xml')
root = tree.getroot()

# print root[0][0].attrib
i1 = 0
while i1 < 10:
    row = root[0][0][i1]
    i2 = 0
    for cell in row:
        if cell.attrib:
            for key,value in cell.attrib.items():
                if 'Index' in key:
                    i2 = int(value) -1
        if i2 == 1: 
            rubrique == cell[0].text
        if i2 == 2:
            subRubrique == cell[0].text
        if i2 == 4:
            company == cell[0].text
        if i2 == 5:
            adress == cell[0].text
        if i2 == 6:
            adress2 == cell[0].text
        if i2 == 7:
            adress3 == cell[0].text
        if i2 == 8:
            zipcode == cell[0].text
        if i2 == 9:
            city == cell[0].text
        if i2 == 10:
            country == cell[0].text
        if i2 == 11:
            tel == cell[0].text
        if i2 == 12:
            fax == cell[0].text
        if i2 == 13:
            email == cell[0].text
        if i2 == 14:
            website == cell[0].text
        try:
            company = Company.objects.get(title=company)
        except:
            company = Company(
                            title=company,
                            adress=adress+' '+adress2+' '+adress3,
                            zipcode=zipcode,
                            city=city,
                            country=country,
                            tel=tel,
                            fax=fax,
                            email=email,
                            website=website,
                        )
            company.save()
        i2 +=1


    i1 +=1
#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from PIL import Image

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
# from django.contrib.auth import logout, login, authenticate, get_backends
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required

from mezzanine.utils.urls import login_redirect, next_url
from mezzanine.pages.models import Page
from .models import *

import xml.etree.ElementTree as ET

def displayCompanies(request):
    if request.POST:
        try:
            cat = request.POST['topic']
            topic = Topic.objects.get(title=cat)
        except:
            return HttpResponse('Aucune catégorie correspondant à l\'entrée')

        # CHECK FOR SUBSIDIARY FIRST TO AVOID REDUNDANCY IN PRINT_FRONT
        redundancyList = []
        allCompanies = Company.objects.filter(topics=topic)
        for company in allCompanies:
            filliales = Subsidiary.objects.filter(top_company=company)
            for filliale in filliales:
                if filliale.sub_company in allCompanies:
                    redundancyList.append(filliale.sub_company.pk)
        # ./

        allCompanies = Company.objects.filter(topics=topic).exclude(pk__in=redundancyList)
        for company in allCompanies:
            company.employees = Person.objects.filter(companies=company)
            for person in company.employees:
                try: 
                    person.job = Job.objects.get(company=company,person=person)
                except:
                    person.job = False

            # product Listing
            company.productList = {}
            for brand in company.brands.all():
                for product in brand.products.all():
                    if not product in company.productList:
                        company.productList[product] = [brand]
                    else:
                        company.productList[product].append(brand)
            # ./

            # FILLIALES [1]
            company.filliales = Subsidiary.objects.filter(top_company=company).order_by('sub_company')
            for filliale in company.filliales:
                # product Listing
                filliale.productList = {}
                for brand in filliale.sub_company.brands.all():
                    for product in brand.products.all():
                        if not product in filliale.productList:
                            filliale.productList[product] = [brand]
                        else:
                            filliale.productList[product].append(brand)
                # ./
                filliale.employees = Person.objects.filter(companies=filliale.sub_company)
                for employee in filliale.employees:
                    try:
                        employee.job = Job.objects.get(company=filliale,person=employees)
                    except:
                        employee.job = False

                # subFILLIALES [2]
                filliale.subFilliales = Subsidiary.objects.filter(top_company=filliale.sub_company).order_by('sub_company')
                for subFilliale in filliale.subFilliales:
                    # product Listing
                    subFilliale.productList = {}
                    for brand in subFilliale.sub_company.brands.all():
                        for product in brand.products.all():
                            if not product in subFilliale.productList:
                                subFilliale.productList[product] = [brand]
                            else:
                                subFilliale.productList[product].append(brand)
                    # ./
                    subFilliale.employees = Person.objects.filter(companies=subFilliale.sub_company)
                    for employee in subFilliale.employees:
                        try: 
                            employee.job = Job.objects.get(company=subFilliale,person=employees)
                        except:
                            employee.job = False
    else:
        allCat = Topic.objects.all()
    return render(request,'displaycompanies.html',locals())


def importPhoto(request):
    # import unicodedata

    yourpath = os.getcwd()
    for root, dirs, files in os.walk('/home/patsykakaz/TABAC/MAIN/receptacle', topdown=False):
        count8 = 0
        countX = 0
        countZ = 0
        for name in files:
            target = os.path.splitext(os.path.join(root, name))[0]
            # target = unicodedata.normalize('NFKD', target).encode('ASCII', 'ignore')
            target = target.split('/')[-1]
            if len(target) == 8:
                count8 += 1
                # print "%s (%s // %s)" % (target,target[:3],target[:-3])
                p1 = Person.objects.filter(firstName__istartswith=target[:3])
                p2 = p1.filter(title__istartswith=target[4:])
                if len(p2) == 1:
                    countZ +=1
                    print p2
                else:
                    print target
                # print "p1Length = %s, p2Length = %s  \n person = %s" % (len(p1),len(p2),p2)
                # print len(p2)
            else:
                countX += 1
        print "count8 = %s \n countX = %s \n countZ = %s" % (count8,countX,countZ)
    return HttpResponse('check console')


def importPhoto(request):
    import unicodedata

    allPersons = Person.objects.filter(illustration__isnull=True)
    i1 = 0
    for element in allPersons:
        composition = ""
        composition += unicodedata.normalize('NFKD', element.firstName).encode('ASCII', 'ignore')[:4]
        composition += unicodedata.normalize('NFKD', element.title).encode('ASCII', 'ignore')[:4]
        # composition = Person.firstName[:3] + Person.title[:3]
        composition = composition.lower()
        if os.path.isfile('/home/patsykakaz/TABAC/MAIN/static/media/uploads/person/import/'+composition+'.jpg'):
            print "FILE IS OK !!!!!!!!!!!!"
            element.illustration = '/static/media/uploads/person/import/'+composition+'.jpg'
            element.save()
            i1 +=1
        else:
            print '%s FILE DOES NOT EXIST' % (composition+'.jpg')
    print len(allPersons)
    print "i1 -> %s" % i1
    return HttpResponse('Check CONSOLE')

def updateImportXML(request):
    tree = ET.parse('liste.xml')
    root = tree.getroot()
    i1 = 0
    while i1 < 2000:
        row = root[0][0][i1]
        i2 = 0
        for cell in row:
            if cell.attrib:
                for key,value in cell.attrib.items():
                    if 'Index' in key:
                        i2 = int(value) -1
            if i2 == 4:
                company = cell[0].text
            if i2 == 8:
                zipcode = cell[0].text
            i2 +=1
        try: 
            company = Company.objects.get(title=company)
            print type(zipcode)
            print company.zipCode
            if zipcode and not company.zipCode:
                company.zipCode = zipcode
                company.save()
        except:
            print "Company %s does not exist" % str(company.title)
        i1 +=1
    return HttpResponse("IMPORT XML process ended.")

def test(request):
    tree = ET.parse('liste.xml')
    root = tree.getroot()
    i1 = 0
    nameList = []
    fullNameList = []
    homonymList = []
    while i1 < 1650:
        row = root[0][0][i1]

        company = False
        person = False
        jobX = False
        rubrique = False
        subRubrique = False
        i2 = 0
        adress = False
        adress2 = False
        adress3 = False
        city = False
        country = False
        tel = False
        fax = False
        email = False
        website = False
        job = False
        person1 = False
        person2 = False
        person_tel = False

        for cell in row:
            if cell.attrib:
                for key,value in cell.attrib.items():
                    if 'Index' in key:
                        i2 = int(value) -1
            # attr = ["rubrique","subRubrique","company","adress",'adress2',"adress3","zipcode","city","country","tel","fax","email","website","job","person1","person2","person_tel"]

            if i2 == 1: 
                rubrique = cell[0].text
            if i2 == 2:
                subRubrique = cell[0].text
            if i2 == 4:
                company = cell[0].text
            if i2 == 5:
                adress = cell[0].text
            if i2 == 6:
                adress2 = cell[0].text
            if i2 == 7:
                adress3 = cell[0].text
            if i2 == 8:
                zipcode = cell[0].text
            if i2 == 9:
                city = cell[0].text
            if i2 == 10:
                country = cell[0].text
            if i2 == 11:
                tel = cell[0].text
            if i2 == 12:
                fax = cell[0].text
            if i2 == 13:
                email = cell[0].text
            if i2 == 14:
                website = cell[0].text
            if i2 == 15:
                job = cell[0].text
            if i2 == 16:
                person1 = cell[0].text
            if i2 == 17:
                person2 = cell[0].text
            if i2 == 18:
                person_tel = cell[0].text
            i2 +=1

            if person1 and person2:
                fullName = person1+person2
                if not person1 in nameList and not fullName in fullNameList:
                    nameList.append(person1)
                    fullNameList.append(fullName)
                elif not fullName in fullNameList:
                    fullNameList.append(fullName)
                    homonymList.append(person1+' '+person2)
                    try: 
                        company = Company.objects.get(title=company)
                        try: 
                            u = Person.objects.filter(Q(title=person1) & Q(firstName=person2))
                            u = u[0]
                        except:
                            u = Person(title=person1,firstName=person2,tel=person_tel)
                            u.save()
                        if job:
                            try:
                                jobX = Job.objects.get(title=job,person=u,company=company)
                            except:
                                jobX = Job(person=u,company=company,title=job)
                                jobX.save()
                    except:
                        print "Company %s does not exist. %s %s is not added ..." % (company,person1,person2)

        i1 +=1
    print len(nameList)
    print len(fullNameList)
    print "homonymList [%s] = %s" % (len(homonymList),homonymList)
    string = "["
    for element in homonymList:
        string += "\""+element+"\", "
    string += "]"
    return HttpResponse(string)

def importXML(request,start,end):
    tree = ET.parse('liste.xml')
    root = tree.getroot()
    i1 = int(start)
    while i1 < int(end):
        row = root[0][0][i1]

        company = False
        person = False
        jobX = False
        rubrique = False
        subRubrique = False
        i2 = 0
        adress = False
        adress2 = False
        adress3 = False
        city = False
        country = False
        tel = False
        fax = False
        email = False
        website = False
        job = False
        person1 = False
        person2 = False
        person_tel = False

        for cell in row:
            if cell.attrib:
                for key,value in cell.attrib.items():
                    if 'Index' in key:
                        i2 = int(value) -1
            if i2 == 1: 
                rubrique = cell[0].text
            if i2 == 2:
                subRubrique = cell[0].text
            if i2 == 4:
                company = cell[0].text
            if i2 == 5:
                adress = cell[0].text
            if i2 == 6:
                adress2 = cell[0].text
            if i2 == 7:
                adress3 = cell[0].text
            if i2 == 8:
                zipcode = cell[0].text
            if i2 == 9:
                city = cell[0].text
            if i2 == 10:
                country = cell[0].text
            if i2 == 11:
                tel = cell[0].text
            if i2 == 12:
                fax = cell[0].text
            if i2 == 13:
                email = cell[0].text
            if i2 == 14:
                website = cell[0].text
            if i2 == 15:
                job = cell[0].text
            if i2 == 16:
                person1 = cell[0].text
            if i2 == 17:
                person2 = cell[0].text
            if i2 == 18:
                person_tel = cell[0].text
            i2 +=1
        try:
            company = Company.objects.get(title=company)
        except:
            company = Company(title=company)
        if adress: 
            company.adress = adress
        if adress2:
            company.adress = company.adress + ' '+ adress2
        if adress3:
            company.adress = company.adress + ' '+ adress3
        if city:
            company.city = city
        if country:
            company.country = country
        if tel:
            company.tel = tel
        if fax:
            company.fax = fax
        if email:
            company.email = email
        if website:
            company.website = website
        company.save()
        if rubrique:
            try:
                topic = Topic.objects.get(title=rubrique)
            except:
                topic = Topic(title=rubrique)
                topic.save()
            company.topics.add(topic)
        if subRubrique:
            try:
                topic = Topic.objects.get(title=subRubrique)
            except:
                topic = Topic(title=subRubrique)
                if rubrique:
                    try:
                        parent = Topic.objects.get(title=rubrique)
                        topic.parent = parent
                    except:
                        pass
                topic.save()
            company.topics.add(topic)
        if person1:
            try: 
                person = Person.objects.get(title=person1)
            except:
                person = Person(title=person1)
                if person2:
                    person.firstName = person2
                if person_tel:
                    person.tel = person_tel
                person.save()
        if job and person:
            try:
                jobX = Job.objects.get(title=job,person=person,company=company)
            except:
                jobX = Job(person=person,company=company,title=job)
                jobX.save()
        # Final Save()
        company.save()

        i1 +=1
    return HttpResponse("IMPORT XML process ended.")



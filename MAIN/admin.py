#-*- coding: utf-8 -*-

from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import *

from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost

# !! PRODUIT !!


class ProductAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets)


brand_fieldsets = deepcopy(PageAdmin.fieldsets)
brand_fieldsets[0][1]["fields"].insert(-1, "products")
brand_fieldsets[0][1]["fields"].insert(-1, "topics")
brand_fieldsets[0][1]["fields"].insert(-1, "illustration")
class BrandAdmin(PageAdmin):
    # add lien rubrique
    fieldsets = brand_fieldsets

class TopicAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets)

class SubsidiaryInline(admin.TabularInline):
    model = Subsidiary
    fk_name = 'top_company'
    extra = 5

class JobInline(admin.TabularInline):
    model = Job
    extra = 5

company_fieldsets = deepcopy(PageAdmin.fieldsets)
company_fieldsets[0][1]["fields"].insert(-1, "brands")
company_fieldsets[0][1]["fields"].insert(-1, "topics")
company_fieldsets[0][1]["fields"].insert(-1, "illustration")
company_fieldsets[0][1]["fields"].insert(-1, "adress")
company_fieldsets[0][1]["fields"].insert(-1, "zipCode")
company_fieldsets[0][1]["fields"].insert(-1, "area")
company_fieldsets[0][1]["fields"].insert(-1, "city")
company_fieldsets[0][1]["fields"].insert(-1, "country")
company_fieldsets[0][1]["fields"].insert(-1, "tel")
company_fieldsets[0][1]["fields"].insert(-1, "fax")
company_fieldsets[0][1]["fields"].insert(-1, "email")
company_fieldsets[0][1]["fields"].insert(-1, "website")
company_fieldsets[0][1]["fields"].insert(-1, "highlight")

class CompanyAdmin(PageAdmin):
    inlines = (JobInline,SubsidiaryInline)
    fieldsets = company_fieldsets


person_fieldsets = deepcopy(PageAdmin.fieldsets)
person_fieldsets[0][1]["fields"].insert(-1, "firstName")
person_fieldsets[0][1]["fields"].insert(-1, "illustration")
person_fieldsets[0][1]["fields"].insert(-1, "adress")
person_fieldsets[0][1]["fields"].insert(-1, "zipCode")
person_fieldsets[0][1]["fields"].insert(-1, "area")
person_fieldsets[0][1]["fields"].insert(-1, "city")
person_fieldsets[0][1]["fields"].insert(-1, "country")
person_fieldsets[0][1]["fields"].insert(-1, "email")
person_fieldsets[0][1]["fields"].insert(-1, "tel")
person_fieldsets[0][1]["fields"].insert(-1, "highlight")
class PersonAdmin(PageAdmin):
    inlines = (JobInline,)
    fieldsets = person_fieldsets

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Company, CompanyAdmin)

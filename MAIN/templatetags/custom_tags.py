from __future__ import unicode_literals

from mezzanine import template
register = template.Library()

@register.filter(name='ExtendCompany')
def ExtendCompany(company, *args):
    print "company pk is -> " + company.pk
    try:
        company = Company.objects.get(pk=company.pk)
    except:
        print "Company fetch Fail"
    print company+"*******"
    return "<h2 style='color:blue';>"OK"</h2>"



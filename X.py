#-*- coding: utf-8 -*-
import os
from PIL import Image
from MAIN.models import *


yourpath = os.getcwd()
for root, dirs, files in os.walk('/Users/patsykakaz_LSC/Desktop/BASE_PHOTOS_OK', topdown=False):
    for name in files:
        target = os.path.splitext(os.path.join(root, name))[0]
        target = target.split('/')[-1]

        person = Person.objects.filter(firstName__startswith=target[:3])
        print person
        # print(os.path.join(root, name))
        # if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
        #     if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
        #         print "A jpeg file already exists for %s" % name
        #     # If a jpeg is *NOT* present, create one from the tiff.
        #     else:
        #         outfile = os.path.splitext(os.path.join('/Users/patsykakaz_LSC/Desktop/receptacle', name))[0] + ".jpg"
        #         try:
        #             im = Image.open(os.path.join(root, name))
        #             print "Generating jpeg for %s" % name
        #             im.thumbnail(im.size)
        #             im.save(outfile, "JPEG", quality=100)
        #         except Exception, e:
        #             print e

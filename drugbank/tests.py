from django.test import TestCase

# Create your tests here.
from drugbank.models import *
from abc import ABCMeta, abstractmethod
import re
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
django.setup()


def find_element():
	drug_all = Drug.objects.all()
	drug_search = drug_all.filter(primaryDrugbankId__contains="1")
	print(drug_search)

def hello(*args):
	for item in args:
		print(args)

if __name__ == '__main__':
	hello("fsdf",2,"fdsf")
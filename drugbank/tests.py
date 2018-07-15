from django.test import TestCase

# Create your tests here.
from drugbank.models import *


def find_element():
	drug_all = Drug.objects.all()
	drug_search = drug_all.filter(primaryDrugbankId__contains="1")
	print(drug_search)


if __name__ == '__main__':
	pass
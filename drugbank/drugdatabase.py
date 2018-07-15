import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
django.setup()

from drugbank.models import *



def find_element():
	drug_all = Drug.objects.all()
	drug_search = drug_all.filter(primaryDrugbankId__contains="1")
	print(drug_search)
	for i in drug_search:
		print(i.primaryDrugbankId)


if __name__ == '__main__':
	find_element()
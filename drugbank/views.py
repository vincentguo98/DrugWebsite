# import os, django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
# django.setup()

from django.shortcuts import render

# Create your views here.
from drugbank import models
from search_class import *
from drugbank.models import *
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

option = Option(projection_=["primaryDrugbankId", "name"],order_=["name","primaryDrugbankId"])



@csrf_exempt
def ProjectionResult(request):
	lis = request.POST.get("index_of_drug")
	print(lis)
	# query = QueryDrug(option)
	# query.setQueryModel(Drug)
	return HttpResponse("0")

@csrf_exempt
def index(request):
	return render(request,'drugbank/index.html',locals())


@csrf_exempt
def search(request):
	return render(request,'drugbank/search.html',locals())




if __name__ == '__main__':
	drug = Drug.objects.all()
	drugdict = {}
	druglist = []
	drugorderedlist = []
	for name in option.projection:
		for i in drug:
			print(eval("i."+name))
			druglist.append(eval("i."+name))
		drugdict[name] = druglist
		druglist = []
	print("-"*20)
	for field in Drug._meta.fields:
		print(field.verbose_name)
	
	
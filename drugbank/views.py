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
	
	lis = request.POST.get("drug")
	druglist = eval(lis)
	print(lis)
	option = Option(projection_ = eval(lis))
	querydrug = QueryDrug(option)
	querydrug.setQueryModel(Drug)
	drug = querydrug.parse()
	print(drug)
	return JsonResponse(drug)

@csrf_exempt
def index(request):
	return render(request,'drugbank/index.html',locals())


@csrf_exempt
def search(request):
	field_name = []
	for field in Drug._meta.fields:
<<<<<<< HEAD
		print(field.verbose_name)
		field_name.append({"field_item_name":field.verbose_name.replace(' ','_')})
=======
		field_name.append({"field_item_name":field.verbose_name.replace(' ',"_")})
>>>>>>> 351c4a16370adb5be76c5fac0fc273655a00fa70
	
	field_dict = {"name":field_name}
	return render(request,'drugbank/search.html',context=field_dict)



#
# if __name__ == '__main__':
# 	drug = Drug.objects.all()
# 	drugdict = {}
# 	druglist = []
# 	drugorderedlist = []
# 	for name in option.projection:
# 		for i in drug:
# 			print(eval("i."+name))
# 			druglist.append(eval("i."+name))
# 		drugdict[name] = druglist
# 		druglist = []
# 	print("-"*20)
# 	for field in Drug._meta.fields:
# 		print(field.verbose_name)
	
	
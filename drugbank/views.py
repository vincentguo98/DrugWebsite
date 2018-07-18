
# import os, django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
# django.setup()

from django.shortcuts import render

# Create your views here.
from drugbank import models
from search_class import *
from drugbank.models import *
from django.http import JsonResponse ,HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def ProjectionResult(request):

    lis = request.POST.get("drug")
    druglist = eval(lis)
    print(lis)
    option = Option(projection_ = eval(lis))
    # querydrug = QueryDrug(option)
    # querydrug.setQueryModel(Drug)
    # drug = querydrug.parse()
    # print(drug)
    # return JsonResponse(drug)
    return HttpResponse("1")
@csrf_exempt
def index(request):
    return render(request ,'drugbank/index.html' ,locals())


@csrf_exempt
def search(request):
    druglist = [Drug ,Pathway ,Category ,Carrier ,Dosage ,SnpAdverseDrugReaction ,Synonym ,SnpEffect ,Salt ,PathwayDrug
                ,Property ,Mixture ,Reaction]
    drugbank_dict = {
        "Drug" :Drug,
        "Pathway" :Pathway,
        "Category" :Category,
        "Carrier" :Carrier,
        "Dosage" :Dosage,
        "SnpAdverseDrugReaction" :SnpAdverseDrugReaction,
        "Synonym" :Synonym,
        "SnpEffect" :SnpEffect,
        "Salt" :Salt,
        "PathwayDrug" :PathwayDrug,
        "Property" :Property,
        "Mixture" :Mixture,
        "Reaction" :Reaction
    }
    field_name = []
    context = []
    for key ,value in drugbank_dict.items():
        for field in value._meta.fields:
            field_name.append(field.verbose_name.replace(' ' ,'_'))
        filed_dict = {key :field_name}
        field_name = []
        context.append(filed_dict)
    dict_example = {"context" :context}
    for table in dict_example["context"]:
        for key ,value in table.items():
            print(key)
            for i in value:
                print(key ,'--' ,i)
    return render(request ,'drugbank/search.html' ,context={"context" :context})



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

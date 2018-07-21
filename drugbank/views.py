
# import os, django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
# django.setup()

from django.shortcuts import render

# Create your views here.
from drugbank import models
from search_class import *
from drugbank.models import *
from django.http import JsonResponse ,HttpResponse,StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from search_class import Option,Querydrugbank


@csrf_exempt
def ProjectionResult(request):

    lis = request.POST.get("drug")
    print(lis)
    print(type(lis))
    option_list = [a.replace('-','.') for a in eval(lis)]
    option = Option(projection_=option_list)
    query = Querydrugbank(option)
    drug_result = {}
    for i in query.Sql_Constrctor():
        for j in i.__dict__:
            if j != "_state":
                drug_result[j] = []
    for i in query.Sql_Constrctor():
        for j in i.__dict__:
            if j != "_state":
                
                if eval("i."+j) is not None:
                    drug_result[j].append(eval("i." + j))
                else:
                    drug_result[j].append("")
    return JsonResponse(drug_result)



@csrf_exempt
def index(request):
    return render(request ,'drugbank/index.html' ,locals())


@csrf_exempt
def search(request):
    druglist = [Drug ,Pathway ,Category ,Carrier ,Dosage ,SnpAdverseDrugReaction ,Synonym ,SnpEffect ,Salt ,PathwayDrug
                ,Property ,Mixture ,Reaction]
    drugbank_dict = {
        "drug" :Drug,
        "pathway" :Pathway,
        "category" :Category,
        "carrier" :Carrier,
        "dosage" :Dosage,
        "snpAdverseDrugReaction" :SnpAdverseDrugReaction,
        "synonym" :Synonym,
        "snpEffect" :SnpEffect,
        "salt" :Salt,
        "pathwaydrug" :PathwayDrug,
        "property" :Property,
        "mixture" :Mixture,
        "reaction" :Reaction
    }
    field_name = []
    context = []
    for key ,value in drugbank_dict.items():
        for field in value._meta.fields:
            itemname = field.verbose_name.replace(' ', '_')
            if itemname != "drug":
                field_name.append(itemname)
            else:
                field_name.append(itemname+"_id")
            print(field_name)
        filed_dict = {key :field_name}
        field_name = []
        context.append(filed_dict)
    return render(request ,'drugbank/search.html' ,context={"context" :context})




@csrf_exempt
def DownloadHandler(request):
    def file_iterator(filename,chunk_size = 512):
        with open("drugbank/example.txt") as f:
            while True:
                c = f.read(chunk_size)
                print(c)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator("example.txt"))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="example.txt"'
    return response



if __name__ == '__main__':
    pass


# import os, django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
# django.setup()

from django.shortcuts import render

# Create your views here.
from drugbank.models import *
from django.http import JsonResponse ,HttpResponse,StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from search_class import Option,Querydrugbank
import numpy as np
import json
import csv
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
    
    data = request.POST.get("download_content")
    data_format = request.POST.get("format_string")
    data_loaded = json.loads(data)
    print(data_format)
    # for json format download ,save as data.json
    if data_format == "json":
        with open("drugbank/data.json",'w') as file:
            json.dump(data_loaded,file)
        file.close()
    
    
    if data_format == "csv":
        data_list = []
        for item in data_loaded:
            for key,value in item.items():
                data_list.append(value)
        print(data_list)
        data_list = map(list,zip(*data_list))
        print(data_list)
        with open('drugbank/data.csv','w') as file:
            writer = csv.writer(file)
            writer.writerows(data_list)
        file.close()
    
        
    if data_format == "txt":
        data_list = []
        content = ""
        for item in data_loaded:
            for key, value in item.items():
                data_list.append(value)
        print(data_list)
        for row in data_list:
            for item in row:
                content+=item+","
            content = content[:-1] + "\n"
        with open('drugbank/data.txt','w') as file:
            file.write(content)
        file.close()
    return HttpResponse(data_format)


def file_iterator(filename,chunk_size=512):
    with open(filename,'r') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def JsonFileDownload(request):
    filename = "drugbank/data.json"
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="data.json"'
    return response
    
def CsvFileDownload(request):
    filename = "drugbank/data.csv"
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="data.csv"'
    return response

def TxtFileDownload(request):
    filename = "drugbank/data.txt"
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="data.txt"'
    return response
    
    





if __name__ == '__main__':
    pass

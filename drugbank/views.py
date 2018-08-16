
import os, django
import pyprind
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
django.setup()

from django.shortcuts import render

# Create your views here.
from drugbank import models
from search_class import *
from drugbank.models import *
from django.http import JsonResponse ,HttpResponse,StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from search_class import Option,Querydrugbank
import pickle
import copy
import functools
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
def search_copy(request):
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
    return render(request ,'drugbank/search(copy).html' ,context={"context" :context})

@csrf_exempt
def search(request):
    # druglist = [Drug ,Pathway ,Category ,Carrier ,Dosage ,SnpAdverseDrugReaction ,Synonym ,SnpEffect ,Salt ,PathwayDrug
    #             ,Property ,Mixture ,Reaction]
    # drugbank_dict = {
    #     "drug" :Drug,
    #     "pathway" :Pathway,
    #     "category" :Category,
    #     "carrier" :Carrier,
    #     "dosage" :Dosage,
    #     "snpAdverseDrugReaction" :SnpAdverseDrugReaction,
    #     "synonym" :Synonym,
    #     "snpEffect" :SnpEffect,
    #     "salt" :Salt,
    #     "pathwaydrug" :PathwayDrug,
    #     "property" :Property,
    #     "mixture" :Mixture,
    #     "reaction" :Reaction
    # }
    # field_name = []
    # context = []
    # for key ,value in drugbank_dict.items():
    #     for field in value._meta.fields:
    #         itemname = field.verbose_name.replace(' ', '_')
    #         if itemname != "drug":
    #             field_name.append(itemname)
    #         else:
    #             field_name.append(itemname+"_id")
    #         print(field_name)
    #     filed_dict = {key :field_name}
    #     field_name = []
    #     context.append(filed_dict)
    druglist = {"drug": "drug", "drug-type":"drug type", "drug-group": "drug group"}
    drug_attr = ["smile", "inchi", "target", "enzyme", "carrier", "transporter", "pathway","drug-drug interaction"]
    drug_type_attr = ["Small Molecule", "Biotech", "All"]
    drug_group_attr = ["Approved", "Nutraceutical", "Illicit", "Investigational", "Withdrawn", "Experimental","Vet_approved","Any"]
    context = []
    context.append({"drug": drug_attr})
    context.append({"drug-type": drug_type_attr})
    context.append({"drug-group": drug_group_attr})
    return render(request ,'drugbank/search.html' ,context={"context" :context, "druglist": druglist})




@csrf_exempt
def DownloadHandler(request):
    def file_iterator(filename,chunk_size = 512):
        with open("drugbank/dataset.txt") as f:
            while True:
                c = f.read(chunk_size)
                print(c)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator("drug.txt"))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="drug.txt"'
    return response

@csrf_exempt
def test(request):
    print(request.POST.getlist("drug"))
    print(request.POST.getlist("drug_group"))
    print(request.POST.get("drug_type"))
    print(request.POST.get("fingerprint"))
    print(request.POST.get("download"))
    return HttpResponse("ok")


def TextShow(request):
    pass

# 通过django的反向查询可以将用统一的形式查询，返回queryset
@csrf_exempt
def filterResult(request):
    
    
    drug_list = request.POST.getlist("drug")
    drug_group = request.POST.getlist("drug_group")
    drug_type = request.POST.get("drug_type")
    request.POST.get("fingerprint")
    request.POST.get("download")
    
    
    drug_filter = DrugFilter()
    
    query_set = drug_filter.defaultFilter(*tuple(drug_list))#获得drug标签的过滤情况
    query_set = drug_filter.stringContainsFilter(type=drug_type.lower())#获得drug type标签的过滤情况
    for item in drug_group:
        query_set = drug_filter.stringContainsFilter(groups=item.lower()) # 获得druggroup标签过滤的情况
    
    drug_extender = DrugDataExtender(query_set)
    for item in drug_list:
        data_set = drug_extender.broadcast(item)
    data = data_set.getResult()
    
    with open("drugbank/dataset.txt","w") as f:
        for line in data:
            f.write('   '.join(line))
            f.write('\n')
    f.close()
    return HttpResponse("ok")







# def _TestForQueryset():
#     drug__filterby_smiles = Drug.objects.filter(smiles__isnull=False)
#     drug__filterby_InChi = drug__filterby_smiles.filter(InChI__isnull=False)
#     drug__filterby_targets = drug__filterby_InChi.filter(drug_targets__isnull=False)
#     drug__filterby_enzymes = drug__filterby_targets.filter(drug_enzymes__isnull=False)
#     drug__filterby_carriers = drug__filterby_enzymes.filter(drug_carriers__isnull=False)
#     drug_filterby_all = drug__filterby_InChi.filter(drug_targets__isnull=False,drug_enzymes__isnull=False,drug_carriers__isnull=False,
#                                 drug_transporters__isnull=False)
#     print(len(drug__filterby_smiles.values_list("primaryDrugbankId",flat=True).distinct()))
#     print(len(drug__filterby_InChi.values_list("primaryDrugbankId",flat=True).distinct()))
#     print(len(drug__filterby_targets.values_list("primaryDrugbankId",flat=True).distinct()))
#     print(len(drug__filterby_enzymes.values_list("primaryDrugbankId",flat=True).distinct()))
#     print(len(drug__filterby_carriers.values_list("primaryDrugbankId",flat=True).distinct()))
#     print('-'*20)
#     print(len(drug__filterby_smiles))
#     print(len(drug__filterby_InChi))
#     print(len(drug__filterby_targets))
#     print(len(drug__filterby_enzymes))
#     print(len(drug__filterby_carriers))
#
#     drug = Drug.objects.all()
#     drug_all_filter = drug.filter(drug_targets__isnull=False)
#     print(len(drug),"-"*20,len(drug_all_filter))
#     for item in drug__filterby_carriers:
#         print(item.drug_targets.all())
#     return drug_filterby_all


def _NameToId():
    
    drug_attr = ["smile", "inchi", "target", "enzyme", "carrier", "transporter", "pathway","drug-drug interaction"]
    name_to_id_dict = {"smile":"smiles","inchi":"InChI","target":"drug_targets","enzyme":"drug_enzymes","carrier":"drug_carriers",
        "transporter":"drug_transporters"}
    with open("name2dict.pickle",'wb') as f:
        pickle.dump(name_to_id_dict,f)
    f.close()






@Name2Field()
def printtest(*args):
    for item in args:
        print(item)

if __name__ == '__main__':
    # _NameToId()
    printtest("smile","inchi")
from django.shortcuts import render

# Create your views here.
from drugbank import models
from drugbank.models import *
from abc import ABCMeta, abstractmethod
import re
import os, django
import pickle
import functools
import copy


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
django.setup()


class ToolKitClass:
    @staticmethod
    def check_instance(instance_type):
        def check_isinstance(instance):
            return isinstance(instance, instance_type)

        return check_isinstance

    @staticmethod
    def isNone(para):
        return (para is None)


def Name2Field(filename="drugbank/name2dict.pickle"):
    def Name2IdDecorate(func):
        with open(filename, 'rb')  as file:
            name2dict = pickle.load(file)
        file.close()
        func_arg = []
        
        @functools.wraps(func)
        def wrapper(self,*args):
            for index, item in enumerate(args):
                if item.lower() in name2dict.keys():
                    func_arg.append(name2dict[item.lower()])
                else:
                    func_arg.append(item)
            return func(self,*tuple(func_arg))
        
        return wrapper
    return Name2IdDecorate


'''
:param
filter : if value between two numbers
contains : search strings which contains give items in contains list
order : specify a display and download sequence
projection : filter the column you need
'''

# projection should be in this format which is drugbank_drug.name
class Option:
    def __init__(self, *, filter_=[], contains_=[], order_=[], projection_=[], **kargs):
        self.filter = filter_
        self.contains = contains_
        self.order = order_
        self.projection = projection_

    @property
    def filter(self):
        return self.filter_

    @filter.setter
    def filter(self, filter_):
        if not ToolKitClass.check_instance(list)(filter_):
            raise Exception("filter's type should be list ")
        if filter_ is None:
            self.filter_ = []
        else:
            self.filter_ = filter_

    @property
    def contains(self):
        return self.contains_

    @contains.setter
    def contains(self, contains_):
        if not ToolKitClass.check_instance(list)(contains_):
            raise Exception("contains's type should be list ")
        if contains_ is None:
            self.contains_ = []
        else:
            self.contains_ = contains_

    @property
    def order(self):
        return self.order_

    @order.setter
    def order(self, order_):
        if not ToolKitClass.check_instance(list)(order_):
            raise Exception("order's type should be list")
        if order_ is None:
            self.order_ = []
        else:
            self.order_ = order_

    @property
    def projection(self):
        return self.projection_

    @projection.setter
    def projection(self, projection_):
        if not ToolKitClass.check_instance(list)(projection_):
            raise Exception("projection's type should be list")
        if projection_ is None:
            self.projection_ = []
        else:
            self.projection_ = projection_

    @property
    def table(self):
        table_list = []
        for projection_name in self.projection:
            if projection_name.split('.')[0] not in table_list:
                table_list.append(projection_name.split('.')[0])
        if "drugbank_drug" not in table_list:
            table_list.append("drugbank_drug")
        return table_list


class Parse(metaclass=ABCMeta):
    @abstractmethod
    def parse(cls):
        pass


class Querydrugbank:
    def __init__(self, option):
        self.filter = option.filter
        self.projection = option.projection
        self.contains = option.contains
        self.table = option.table
        self.queryset = []
        self.querydict = {}
        self.Sql_projection = ""
        self.Sql_From = ""
        self.Sql_Default_Where = ""

    def _getQuerySetAll(self):
        return self.modeltype.objects.all()

    def setQueryModel(self, modeltype):
        self.modeltype = modeltype

    # 	generate the projection sql just after select
    @property
    def Sql_Projection_generator(self):
        self.Sql_projection = ""
        if "drugbank_drug.primaryDrugbankId" not in self.projection:
            self.projection.append("drugbank_drug.primaryDrugbankId")
        for sql in self.projection:
            self.Sql_projection += sql + ","
        self.Sql_projection = " " + self.Sql_projection[:-1] + " "
        return self.Sql_projection

    # QueryResultSet = Drug.objects.raw(
    # 	"select drugbank_drug.primaryDrugbankId,drugbank_dosage.drug_id, drugbank_category.drug_id, drugbank_drug.name,unii,form from drugbank_drug ,drugbank_dosage,drugbank_category  WHERE drugbank_drug.primaryDrugbankId=drugbank_dosage.drug_id AND drugbank_category.drug_id = drugbank_drug.primaryDrugbankId")
    # return QueryResultSet
    @property
    def Sql_From_generator(self):
        self.Sql_From = ""
        if "drugbank_drug" not in self.table:
            self.table.append("drugbank_drug")
        for sql in self.table:
            self.Sql_From += sql + ","
        self.Sql_From = " " + self.Sql_From[:-1] + " "
        return self.Sql_From

    @property
    def Sql_Default_Where_generator(self):
        self.Sql_Default_Where = ""
        for sql in self.table:
            if sql == "drugbank_drug":
                continue
            else:
                self.Sql_Default_Where += "drugbank_drug.primaryDrugbankId=" + sql + ".drug_id" + " AND "
        self.Sql_Default_Where = self.Sql_Default_Where[:-4]
        return " " + self.Sql_Default_Where + " "

    def Sql_Constrctor(self):
        sql = "select" + self.Sql_Projection_generator + "from" + self.Sql_From_generator
        if self.Sql_Default_Where_generator != "  ":
            sql +=  "where" + self.Sql_Default_Where_generator
        Querydrugbank = Drug.objects.raw(sql)
        return Querydrugbank

    def parse(self):
        _filter = self.option.filter
        _contains = self.option.contains
        _projection = self.option.projection
        queryset = self._getQuerySetAll()
        drugdict = {}
        druglist = []
        for name in _projection:
            for i in queryset:
                druglist.append(eval("i." + name))
            drugdict[name] = druglist
            druglist = []
        return drugdict


'''
generate option class to feed


'''


class Option_factory:
    def __init__(self, parse):
        self.parse = []
        self.option = Option()

    def register(self, parse):
        if parse not in self.parse:
            self.parse.append(parse)
        else:
            raise Warning("already register a similar parse")
        self.parse = parse
        return self.get_option()

    def get_option(self):
        for parse in self.parse:
            self.option = parse.parse(self.option)
        return self.option


class ParseSelector:
    def __init__(self, request):
        pass



class DrugFilter:
    
    def __init__(self):
        self.queryset = Drug.objects.filter(primaryDrugbankId__isnull=False)
        
    
    @Name2Field()
    def registerFilter(self,*args):
        for index,item in enumerate(args):
            self.queryset = eval("self.queryset."+"filter("+ item +")")
        return self.queryset
    
    
    
    
    def stringContainsFilter(self,**kargs):
        print(len(self.queryset))
        for key, value in kargs.items():
            if value not in ["small molecule","biotech","approved", "nutraceutical", "illicit",
                           "investigational", "withdrawn", "experimental","vet_approved"]:
                print("not excuted")
                continue
            parameter = str(key)+"__contains"
            dic = {parameter:value}
            self.queryset = self.queryset.filter(**dic)
        return self.queryset
 
 
    
    @Name2Field()
    def defaultFilter(self,*args):
        str_values = "primaryDrugbankId"
        str_values_list = ["primaryDrugbankId"]
        for index,item in enumerate(args):
            str = "self.queryset." + "filter(" + item + "__isnull=False" + ")"
            print(str)
            self.queryset = eval("self.queryset."+"filter("+ item+"__isnull=False" +")")
            
            if item in ["smiles","InChI"]:
                str_values_list.append(item)
        self.queryset = self.queryset.values(*tuple(str_values_list)).distinct()
        disctinct_query = []
        for item in self.queryset:
            if item not in disctinct_query:
                disctinct_query.append(item)
        self.queryset = Drug.objects.filter(primaryDrugbankId__in=[item["primaryDrugbankId"] for item in disctinct_query])
        return self.queryset
    
    def getQueryset(self):
        return self.queryset
    




class DrugDataExtender():
    
    def __init__(self,drug_queryset,*args):
        self.drug_queryset = drug_queryset
        self.dataset = [[drug,drug.primaryDrugbankId] for drug in self.drug_queryset]
        
    def broadcast(self,entity_name):
        temp = []
        if entity_name == "target":
            for inner_list in self.dataset:
                for entity in inner_list[0].drug_targets.all():
                    sub_data = copy.deepcopy(inner_list)
                    sub_data.append(entity.id)
                    temp.append(sub_data)
            self.dataset = temp
            return self
        
        if entity_name == "enzyme":
            for  inner_list in self.dataset:
                for entity in inner_list[0].drug_enzymes.all():
                    sub_data = copy.deepcopy(inner_list)
                    sub_data.append(entity.id)
                    temp.append(sub_data)
            self.dataset = temp
            return self
            
        if entity_name == "carrier":
            for inner_list in self.dataset:
                for entity in inner_list[0].drug_carriers.all():
                    sub_data = copy.deepcopy(inner_list)
                    sub_data.append(entity.id)
                    temp.append(sub_data)
            self.dataset = temp
            return self
        
        if entity_name == "transporter":
            for inner_list in self.dataset:
                for entity in inner_list[0].drug_transporters.all():
                    sub_data = copy.deepcopy(inner_list)
                    sub_data.append(entity.id)
                    temp.append(sub_data)
            self.dataset = temp
            return self
        
        if entity_name == "smile":
            for inner_list in self.dataset:
                inner_list.append(inner_list[0].smiles)
            return self
            
        if entity_name == "inchi":
            for inner_list in self.dataset:
                inner_list.append(inner_list[0].InChI)
            return self
        
        else:
            print("some error happens")
            return self
        
    def getResult(self):
        return [inner_list[1:] for inner_list in self.dataset]
        
       
        
        





if __name__ == '__main__':
    pass




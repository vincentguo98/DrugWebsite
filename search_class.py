from django.shortcuts import render

# Create your views here.
from drugbank import models
from drugbank.models import *
from abc import ABCMeta, abstractmethod
import re
import os, django

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
        sql = "select" + self.Sql_Projection_generator + "from" + self.Sql_From_generator + "where" + self.Sql_Default_Where_generator
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


if __name__ == '__main__':
    pass




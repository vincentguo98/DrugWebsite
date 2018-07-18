import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrugWebsite.settings")
django.setup()

from drugbank.models import *
from search_class import Querydrugbank, Option


def find_element():
    drug_all = Drug.objects.all()
    drug_search = drug_all.filter(primaryDrugbankId__contains="1")
    print(drug_search)
    for i in drug_search:
        print(i.primaryDrugbankId)


def example():
    option = Option()
    querydrug = Querydrugbank(option)
    result = querydrug.Sql_Projection_generator()
    for i in result:
        # print(i.form + "---" + i.primaryDrugbankId)
        print(i.primaryDrugbankId)
        print(i)
        print(i.__dict__)
    print(result)


if __name__ == '__main__':
    # example()
    option = Option(
        projection_=["drugbank_drug.alternativeDrugbankId", "drugbank_drug.name", "drugbank_category.category",
                     "drugbank_salt.unii", "drugbank_drug.unii"])
    query = Querydrugbank(option)
    print(query.Sql_Projection_generator)
    print(query.Sql_From_generator)
    print(query.Sql_Default_Where_generator)
    query_set = query.Sql_Constrctor()
    for i in query_set:
        for j in i.__dict__:
            if j != "_state":
                if eval("i." + j) is not None:
                    print(j + ":" + eval("i." + j))
                else:
                    print(j + ":" + "")
        # print(j + ":" +eval("i."+j))
        print("-" * 20)





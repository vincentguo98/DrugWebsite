import ast
from django.db import models


# import ast
#
# from django.db import models
#
#
# # Create your models here.
#
#
class ListField(models.TextField):
	"""
    存储字符串列表的类
    """
	
	def __init__(self, *args, **kwargs):
		super(ListField, self).__init__(*args, **kwargs)
	
	def to_python(self, value):
		if not value:
			return []
		if isinstance(value, list):
			return value
		return ast.literal_eval(value)
	
	def get_prep_value(self, value):
		if value is None:
			return value
		return str(value)


#
#
# class Drug(models.Model):
#     """
#     主类，用来生成药物
#     主键：drugbankId
#     """
#     primaryDrugbankId = models.TextField(primary_key=True, default='')
#     alternativeDrugbankId = ListField(default=[])
#     # drugbank第一个为primary的
#     # drugbankId 可以有多个，但是只有一个是primary的。就比如Lepirudin有DB00001\BTD00024\BI0D00024
#     # 三种。具体怎么安排不明，但是primary只有DB00001
#     name = models.TextField()  # type: str
#     # description = models.TextField(null=True)  # type: str
#     casNumber = models.TextField(null=True)  # type: str
#     unii = models.TextField(null=True)  # type: str
#     state = models.TextField(null=True)  # type: str
#     groups = ListField(null=True)  # type: list[str]
#     # synthesisReference = models.TextField(null=True)  # type: str
#     # indication = models.TextField(null=True)
#     # pharmacodynamics = models.TextField(null=True)
#     # mechanismOfAction = models.TextField(null=True)
#     toxicity = models.TextField(null=True)
#     metabolism = models.TextField(null=True)
#     # absorption = models.TextField(null=True)
#     halfLife = models.TextField(null=True)
#     proteinBinding = models.TextField(null=True)  # type: str
#     # routeOfElimination = models.TextField(null=True)
#     volumeOfDistribution = models.TextField(null=True)
#     clearance = models.TextField(null=True)
#     affectedOrganisms = ListField(null=True)  # type: list[AffectedOrganism]
#     ahfsCodes = models.TextField(null=True)
#     pdbEntries = models.TextField(null=True)
#     fdaLabel = models.TextField(null=True)
#     msds = models.TextField(null=True)
#     foodInterations = ListField(null=True)  # type: # list[FoodInteraction] todo: change it to table
#     sequences = ListField(null=True)  # type: # list[str] format一直都是FASTA吗
#     enzymes = ListField(null=True)  # type: # list[str]
#     atcCodes = ListField(null=True)
#     synonyms = ListField(null=True)
#     classfication_description = models.TextField(null=True)
#     classfication_directParent = models.TextField(null=True)
#     classfication_kingdom = models.TextField(null=True)
#     classfication_superclass = models.TextField(null=True)
#     classfication_kls = models.TextField(null=True)
#     classfication_subclass = models.TextField(null=True)
#     classfication_alternativeParents = ListField(null=True)
#     classfication_substituent = ListField(null=True)
# """
# 类划分原则:
# 1. 描述药物属性的属弱实体，没有主键，如Dosage
# 2. 描述角色的属强实体，有主键
# """
#
#
# # region 强实体
# # todo: distinguish it is weak entity or strong entity
# # 强实体？？？
# class Pathway(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_pathways")
#     smpdbId = models.TextField(primary_key=True)
#     name = models.TextField(null=True)
#     category = models.TextField(null=True)
#     enzymes = ListField(null=True)
#
#
# # 多肽，强实体
# class Polypeptide(models.Model):
#
#     pid = models.TextField(default="")
#     source = models.TextField(null=True)
#     name = models.TextField(null=True)
#     generalFunction = models.TextField(null=True)
#     specificFunction = models.TextField(null=True)
#     geneName = models.TextField(null=True)
#     locus = models.TextField(null=True)
#     cellularLocation = models.TextField(null=True)
#     transmembraneRegions = models.TextField(null=True)
#     signalRegions = models.TextField(null=True)
#     theoreticalPi = models.TextField(null=True)
#     molecularWeight = models.TextField(null=True)
#     chromosomeLocation = models.TextField(null=True)
#     organism = models.TextField(null=True)
#     organismNcbiTaxonomyId = models.TextField(null=True)
#     aminoAcidSequence = models.TextField(null=True)
#     geneSequence =  models.TextField(null=True)
#     externalIdentifiers = models.TextField(null=True)
#     synonyms = ListField(null=True)
#
#
# # 强实体
# class Category(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_categories")
#     category = models.TextField(primary_key=True)
#     meshId = models.TextField(null=True)
#
#
# # 强实体
# class Protein(models.Model):
#     id = models.TextField(primary_key=True, default='')
#     name = models.TextField(null=True)
#     organism = models.TextField(null=True)
#     # textbooks = models.ForeignKey(Textbook, on_delete=models.DO_NOTHING, related_name="textBookRecord_protein")
#     # related_name="articleRecord_protein") #todo: this is wrong
#     action = ListField(null=True)
#     knownAction = models.TextField(null=True)
#     polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING, unique=False)
#
#
# # 强实体
# class Carrier(models.Model):
#     drug = models.ManyToManyField(Drug, related_name="drug_carriers")
#     id = models.TextField(primary_key=True, default="")
#     name = models.TextField(null=True)
#     organism = models.TextField(null=True)
#     action = ListField(null=True)
#     knownAction = models.TextField(null=True)
#     polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING, null=True, unique=False)
#
#
# # 强实体
# class Transporter(models.Model):
#     drug = models.ManyToManyField(Drug, related_name="drug_transporters")
#     id = models.TextField(primary_key=True, default='')
#     name = models.TextField(null=True)
#     organism = models.TextField(null=True)
#     action = ListField(null=True)
#     knownAction = models.TextField(null=True)
#     polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING, null=True, unique=False)
#
#
# # 强实体
# class Target(models.Model):
#     drug = models.ManyToManyField(Drug, related_name="drug_targets")
#     id = models.TextField(primary_key=True, default='')
#     name = models.TextField(null=True)
#     organism = models.TextField(null=True)
#     action = ListField(null=True)
#     knownAction = models.TextField(null=True)
#     polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING, null=True, unique=False)
#
#
# # 强实体
# class Enzyme(models.Model):
#     drug = models.ManyToManyField(Drug, related_name="drug_enzymes")
#     id = models.TextField(primary_key=True, default='')
#     name = models.TextField(null=True)
#     organism = models.TextField(null=True)
#     action = ListField(null=True)
#     knownAction = models.TextField(null=True)
#     polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING, null=True)
#
#
# # endregion
#
# # region 弱实体
#
# # 剂量，属弱实体
# class Dosage(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_dosages")
#     form = models.TextField(null=True)
#     route = models.TextField(null=True)
#     strength = models.TextField(null=True)
#
#
# # 不良反应，属弱实体
# class SnpAdverseDrugReaction(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_snpAdverseDrugReactions")
#     proteinName = models.TextField(null=True)
#     geneSymbol = models.TextField(null=True)
#     uniprotId = models.TextField(null=True)
#     rsId = models.TextField(null=True)
#     allele = models.TextField(null=True)
#     adverseReaction = models.TextField(null=True)
#     definingChange = models.TextField(null=True)
#     description = models.TextField(null=True)
#     pubmedId = models.TextField(null=True)
#
#
# # 弱实体
# class Synonym(models.Model):
#     # todo: coverage with drug and become ListField
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_synonym")
#     content = models.TextField(null=True)
#     language = models.TextField(null=True)
#     coder = models.TextField(null=True)
#
#
# # 效果，属弱实体
# class SnpEffect(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_snpEffects")
#     proteinName = models.TextField(null=True)
#     geneSymbol = models.TextField(null=True)
#     uniprotId = models.TextField(null=True)
#     rsId = models.TextField(null=True)
#     allele = models.TextField(null=True)
#     definingChange = models.TextField(null=True)
#     description = models.TextField(null=True)
#     pubmedId = models.TextField(null=True)
#
#
# # todo: distinguish it is weak entity or strong entity
# # 看上去是……弱实体
# class Salt(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_salt")
#     drugbankId = ListField(null=True)  # type: list[str]
#     name = models.TextField(null=True)
#     unii = models.TextField(null=True)
#     casNumber = models.TextField(null=True)
#     inchikey = models.TextField(null=True)
#
#
# # what the hell?去分类器
# class GoClassifier(models.Model):
#     polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, related_name="polypeptide_goClassifiers")
#     category = models.TextField(null=True)
#     description = models.TextField(null=True)
#
#
# # 蛋白质家族数据库(我觉得应该是描述药物的吧)
# class Pfam(models.Model):
#     polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, related_name="polypeptide_pfams")
#
#     identifier = models.TextField(null=True)
#     name = models.TextField(null=True)
#
#
# # 弱实体
# class ExternalIdentifier(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_externalIdentifiers")
#     resource = models.TextField(null=True)
#     identifier = models.TextField(null=True)
#
#
# # 弱实体
# class PolypeptideExternalIdentifier(models.Model):
#     polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING,
#                                     related_name="polypeptide_externalIdentifiers")
#     resource = models.TextField(null=True)
#     identifier = models.TextField(null=True)
#
#
# # 弱得一比吧这……
# class PathwayDrug(models.Model):
#     pathway = models.ForeignKey(Pathway, on_delete=models.DO_NOTHING, related_name="pathway_Drugs")
#     drugbankId = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_asPathwayDrug")
#     name = models.TextField(null=True)
#
#
# class Property(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_properties")
#
#     kind = models.TextField(null=True)
#     value = models.TextField(null=True)
#     source = models.TextField(null=True)
#
#
# # todo: please fix it? or identify it
# # 这个本应该是两个外键的一张表，但是这个并不好保存
# # 我就这么存了
# class DrugInteraction(models.Model):
#     drug1 = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug1_drugInteractions")
#     drug2 = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug2_drugInteractions")
#
#     # drugbankId = models.TextField(null=True)
#     # name = models.TextField(null=True)
#     # description = models.TextField(null=True)
#
#
# # # 我觉得应该是弱实体来着
# # class AtcCode(models.Model):
# #     # todo: coverage with Drug, become TextField with code of atc-code
# #     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_atcCodes")
# #     code = models.TextField(null=True)
#
#
# # 我觉得应该是弱实体来着
# # class Level(models.Model):
# #     atcCode = models.ForeignKey(AtcCode, on_delete=models.DO_NOTHING, related_name="atcCode_levels")
# #     code = models.TextField(null=True)
# #     content = models.TextField(null=True)
#
#
# # 弱实体
# class Mixture(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_mixtures")
#
#     name = models.TextField()
#     ingredients = models.TextField(null=True)
#
#
# # 弱实体
# # class Classification(models.Model):
# #     drug = models.OneToOneField(Drug, on_delete=models.DO_NOTHING)
# #     # todo: add field alternative-parent ListField & substituent ListField
# #     description = models.TextField(null=True)
# #     directParent = models.TextField(null=True)
# #     kingdom = models.TextField(null=True)
# #     superclass = models.TextField(null=True)
# #     kls = models.TextField(null=True)
# #     subclass = models.TextField(null=True)
# #     alternativeParents = ListField(null=True)
# #     substituent = ListField(null=True)
# #
# # 弱
# class Reaction(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drugs_reactions")
#     seqence = models.IntegerField(null=True, default=-1)
#     left_element = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drugs_asLeft_reactions")
#     right_element = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drugs_asRight_reactions")
#
#
# # 弱
# class ReactionEnzyme(models.Model):
#     reaction = models.ForeignKey(Reaction, on_delete=models.DO_NOTHING, related_name="reaction_enzymes")
#     drugbankId = models.TextField(null=True)
#     name = models.TextField(null=True)
#     uniprotId = models.TextField(null=True)
#
# # endregion 弱实体



# Create your models here.


class ListField(models.TextField):
	"""
    存储字符串列表的类
    """
	
	def __init__(self, *args, **kwargs):
		super(ListField, self).__init__(*args, **kwargs)
	
	def to_python(self, value):
		if not value:
			return []
		if isinstance(value, list):
			return value
		return ast.literal_eval(value)
	
	def get_prep_value(self, value):
		if value is None:
			return value
		return str(value)


# 2018.8.12修改 Drug增加 smiles，InChi,

class Drug(models.Model):
	"""
    主类，用来生成药物
    主键：drugbankId
    """
	primaryDrugbankId = models.CharField(primary_key=True, default='', max_length=20)
	alternativeDrugbankId = ListField(default=[])
	# drugbank第一个为primary的
	# drugbankId 可以有多个，但是只有一个是primary的。就比如Lepirudin有DB00001\BTD00024\BI0D00024
	# 三种。具体怎么安排不明，但是primary只有DB00001
	name = models.TextField()  # type: str
	# description = models.TextField(null=True)
	# description = models.TextField(null=True)  # type: str
	casNumber = models.TextField(null=True)  # type: str
	unii = models.TextField(null=True)  # type: str
	state = models.TextField(null=True)  # type: str
	groups = ListField(null=True)  # type: list[str]
	# synthesisReference = models.TextField(null=True)  # type: str
	# indication = models.TextField(null=True)
	# pharmacodynamics = models.TextField(null=True)
	# mechanismOfAction = models.TextField(null=True)
	toxicity = models.TextField(null=True)
	metabolism = models.TextField(null=True)
	# absorption = models.TextField(null=True)
	halfLife = models.TextField(null=True)
	proteinBinding = models.TextField(null=True)  # type: str
	# routeOfElimination = models.TextField(null=True)
	volumeOfDistribution = models.TextField(null=True)
	clearance = models.TextField(null=True)
	affectedOrganisms = ListField(null=True)  # type: list[AffectedOrganism]
	ahfsCodes = models.TextField(null=True)
	pdbEntries = models.TextField(null=True)
	fdaLabel = models.TextField(null=True)
	msds = models.TextField(null=True)
	sequences = ListField(null=True)  # type: # list[str] format一直都是FASTA吗
	enzymes = ListField(null=True)  # type: # list[str]
	atcCodes = ListField(null=True)
	synonyms = ListField(null=True)
	classfication_description = models.TextField(null=True)
	classfication_directParent = models.TextField(null=True)
	classfication_kingdom = models.TextField(null=True)
	classfication_superclass = models.TextField(null=True)
	classfication_kls = models.TextField(null=True)
	classfication_subclass = models.TextField(null=True)
	classfication_alternativeParents = ListField(null=True)
	classfication_substituent = ListField(null=True)
	smiles = models.TextField(null=True)
	InChI = models.TextField(null=True)


"""
类划分原则:
1. 描述药物属性的属弱实体，没有主键，如Dosage
2. 描述角色的属强实体，有主键
"""


# region 强实体
# todo: distinguish it is weak entity or strong entity
# 强实体？？？

# 2018/8/12 修改 去掉有关drug的外键，使得pathway成为一个独立的关系
# 关系 共有两个实体参与 drug,enzymes,多对多关系
# 外键 无外键
class Pathway(models.Model):
	# drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_pathways")
	smpdbId = models.CharField(primary_key=True, max_length=30)
	name = models.TextField(null=True)
	category = models.TextField(null=True)
	pathway_drugs_id = ListField(null=True)
	enzymes_uniprot_id = ListField(null=True)


# 多肽，强实体
# 暂时不用
class Polypeptide(models.Model):
	pid = models.TextField(default="")
	source = models.TextField(null=True)
	name = models.TextField(null=True)
	generalFunction = models.TextField(null=True)
	specificFunction = models.TextField(null=True)
	geneName = models.TextField(null=True)
	locus = models.TextField(null=True)
	cellularLocation = models.TextField(null=True)
	transmembraneRegions = models.TextField(null=True)
	signalRegions = models.TextField(null=True)
	theoreticalPi = models.TextField(null=True)
	molecularWeight = models.TextField(null=True)
	chromosomeLocation = models.TextField(null=True)
	organism = models.TextField(null=True)
	organismNcbiTaxonomyId = models.TextField(null=True)
	aminoAcidSequence = models.TextField(null=True)
	geneSequence = models.TextField(null=True)
	externalIdentifiers = models.TextField(null=True)
	synonyms = ListField(null=True)


# 强实体
class Category(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_categories")
	category = models.TextField(null=True)
	meshId = models.TextField(null=True)


# 强实体
class Protein(models.Model):
	id = models.CharField(primary_key=True, default='', max_length=20)
	name = models.TextField(null=True)
	organism = models.TextField(null=True)
	# textbooks = models.ForeignKey(Textbook, on_delete=models.DO_NOTHING, related_name="textBookRecord_protein")
	# related_name="articleRecord_protein") #todo: this is wrong
	action = ListField(null=True)
	knownAction = models.TextField(null=True)
	polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING, unique=False)


# 强实体
class Carrier(models.Model):
	drug = models.ManyToManyField(Drug, related_name="drug_carriers")
	id = models.CharField(primary_key=True, default="", max_length=20)
	name = models.TextField(null=True)
	organism = models.TextField(null=True)
	action = ListField(null=True)
	knownAction = models.TextField(null=True)
	polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, null=True, unique=False)


# 强实体
class Transporter(models.Model):
	drug = models.ManyToManyField(Drug, related_name="drug_transporters")
	id = models.CharField(primary_key=True, default='', max_length=20)
	name = models.TextField(null=True)
	organism = models.TextField(null=True)
	action = ListField(null=True)
	knownAction = models.TextField(null=True)
	polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, null=True, unique=False)


# 强实体
class Target(models.Model):
	drug = models.ManyToManyField(Drug, related_name="drug_targets")
	id = models.CharField(primary_key=True, default='', max_length=20)
	name = models.TextField(null=True)
	organism = models.TextField(null=True)
	action = ListField(null=True)
	knownAction = models.TextField(null=True)
	polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, null=True, unique=False)


# 强实体
class Enzyme(models.Model):
	drug = models.ManyToManyField(Drug, related_name="drug_enzymes")
	id = models.CharField(primary_key=True, default='', max_length=20)
	name = models.TextField(null=True)
	organism = models.TextField(null=True)
	action = ListField(null=True)
	knownAction = models.TextField(null=True)
	polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, null=True)


# endregion

# region 弱实体

# 剂量，属弱实体
class Dosage(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_dosages")
	form = models.TextField(null=True)
	route = models.TextField(null=True)
	strength = models.TextField(null=True)


# 不良反应，属弱实体
class SnpAdverseDrugReaction(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_snpAdverseDrugReactions")
	proteinName = models.TextField(null=True)
	geneSymbol = models.TextField(null=True)
	uniprotId = models.TextField(null=True)
	rsId = models.TextField(null=True)
	allele = models.TextField(null=True)
	adverseReaction = models.TextField(null=True)
	definingChange = models.TextField(null=True)
	description = models.TextField(null=True)
	pubmedId = models.TextField(null=True)


# 弱实体
class Synonym(models.Model):
	# todo: coverage with drug and become ListField
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_synonym")
	content = models.TextField(null=True)
	language = models.TextField(null=True)
	coder = models.TextField(null=True)


# 效果，属弱实体
class SnpEffect(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_snpEffects")
	proteinName = models.TextField(null=True)
	geneSymbol = models.TextField(null=True)
	uniprotId = models.TextField(null=True)
	rsId = models.TextField(null=True)
	allele = models.TextField(null=True)
	definingChange = models.TextField(null=True)
	description = models.TextField(null=True)
	pubmedId = models.TextField(null=True)


# todo: distinguish it is weak entity or strong entity
# 看上去是……弱实体
class Salt(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_salt")
	drugbankId = ListField(null=True)  # type: list[str]
	name = models.TextField(null=True)
	unii = models.TextField(null=True)
	casNumber = models.TextField(null=True)
	inchikey = models.TextField(null=True)


# what the hell?去分类器
class GoClassifier(models.Model):
	polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, related_name="polypeptide_goClassifiers")
	category = models.TextField(null=True)
	description = models.TextField(null=True)


# 蛋白质家族数据库(我觉得应该是描述药物的吧)
class Pfam(models.Model):
	polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, related_name="polypeptide_pfams")
	
	identifier = models.TextField(null=True)
	name = models.TextField(null=True)


# 弱实体
class ExternalIdentifier(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_externalIdentifiers")
	resource = models.TextField(null=True)
	identifier = models.TextField(null=True)


# 弱实体
class PolypeptideExternalIdentifier(models.Model):
	polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING,
	                                related_name="polypeptide_externalIdentifiers")
	resource = models.TextField(null=True)
	identifier = models.TextField(null=True)


# 弱得一比吧这……
class PathwayDrug(models.Model):
	pathway = models.ForeignKey(Pathway, on_delete=models.DO_NOTHING, related_name="pathway_Drugs")
	drugbankId = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_asPathwayDrug")
	name = models.TextField(null=True)


class Property(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_properties")
	kind = models.TextField(null=True)
	value = models.TextField(null=True)
	source = models.TextField(null=True)


# todo: please fix it? or identify it
# 这个本应该是两个外键的一张表，但是这个并不好保存
# 我就这么存了
# xml解析出来的id,解析出来的Drug没有与之对应的
class DrugInteraction(models.Model):
	drug1 = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug1_drugInteractions", null=True,
	                          blank=True)
	drug2 = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug2_drugInteractions", null=True,
	                          blank=True)
	drug2_alternative_id = models.TextField(null=True)
	
	# drugbankId = models.TextField(null=True)
	# name = models.TextField(null=True)
	# description = models.TextField(null=True)


# # 我觉得应该是弱实体来着
# class AtcCode(models.Model):
#     # todo: coverage with Drug, become TextField with code of atc-code
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_atcCodes")
#     code = models.TextField(null=True)


# 我觉得应该是弱实体来着
# class Level(models.Model):
#     atcCode = models.ForeignKey(AtcCode, on_delete=models.DO_NOTHING, related_name="atcCode_levels")
#     code = models.TextField(null=True)
#     content = models.TextField(null=True)


# 弱实体
class Mixture(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_mixtures")
	
	name = models.TextField()
	ingredients = models.TextField(null=True)


# 弱实体
# class Classification(models.Model):
#     drug = models.OneToOneField(Drug, on_delete=models.DO_NOTHING)
#     # todo: add field alternative-parent ListField & substituent ListField
#     description = models.TextField(null=True)
#     directParent = models.TextField(null=True)
#     kingdom = models.TextField(null=True)
#     superclass = models.TextField(null=True)
#     kls = models.TextField(null=True)
#     subclass = models.TextField(null=True)
#     alternativeParents = ListField(null=True)
#     substituent = ListField(null=True)
#
# 弱
class Reaction(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drugs_reactions")
	seqence = models.IntegerField(null=True, default=-1)
	left_element = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drugs_asLeft_reactions")
	right_element = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drugs_asRight_reactions")


# 弱
class ReactionEnzyme(models.Model):
	reaction = models.ForeignKey(Reaction, on_delete=models.DO_NOTHING, related_name="reaction_enzymes")
	drugbankId = models.TextField(null=True)
	name = models.TextField(null=True)
	uniprotId = models.TextField(null=True)

# endregion 弱实体

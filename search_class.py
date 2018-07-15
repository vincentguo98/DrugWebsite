from django.shortcuts import render

# Create your views here.
from drugbank import models
from drugbank.models import *
from abc import ABCMeta, abstractmethod


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





class Parse(metaclass=ABCMeta):
	@abstractmethod
	def parse(cls):
		pass




class QueryDrug:
	def __init__(self,option):
		self.option = option
		
		
	def _getQuerySetAll(self):
		return self.modeltype.objects.all()
		
	def setQueryModel(self,modeltype):
		self.modeltype = modeltype
	
	def parse(self):
		_filter = self.option.filter
		_contains = self.option.contains
		_projection = self.option.projection
		queryset = self._getQuerySetAll()
		drugdict = {}
		druglist = []
		for name in _projection:
			for i in queryset:
				druglist.append(eval("i."+name))
			drugdict[name] = druglist
			druglist = []
		return drugdict
	
		
'''
generate option class to feed


'''
		
class Option_factory:
	def __init__(self,parse):
		self.parse = parse
	
	def register(self,parse):
		self.parse = parse
		return self.get_option()
		
	def get_option(self):
		option = self.parse.parse()
		
		
		
		
		
		
		
		
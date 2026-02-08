# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib import admin

from apps.common_functions import get_dev_num_str

import logging
logger = logging.getLogger('django')


class FilterDataDevNum(admin.SimpleListFilter):

	parameter_name = 'data_dev_num'

	def title(self):
		return "Dev num"

	def lookups(self, request, model_admin):
		return (
			('0', "-"),
			('1', get_dev_num_str(1)),
			('2', get_dev_num_str(2)),
			('3', get_dev_num_str(3)),
			('4', get_dev_num_str(4)),
			('5', get_dev_num_str(5)),
		)

	def queryset(self, request, queryset):
		if self.value() == '0':
			return queryset.filter(data_dev_num=0)
		if self.value() == '1':
			return queryset.filter(data_dev_num=1)
		if self.value() == '2':
			return queryset.filter(data_dev_num=2)
		if self.value() == '3':
			return queryset.filter(data_dev_num=3)
		if self.value() == '4':
			return queryset.filter(data_dev_num=4)
		if self.value() == '5':
			return queryset.filter(data_dev_num=5)
		return queryset


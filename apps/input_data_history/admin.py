# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib import admin
from .models import InputDataHistory
from rangefilter.filters import DateRangeFilter
from django.utils.html import format_html

from apps.common_functions import get_dev_num_str
from apps.custom_admin import CustomAdmin
from .admin_filters import FilterDataDevNum


@admin.register(InputDataHistory)
class InputDataHistoryAdmin(CustomAdmin):

	class Media:
		js = CustomAdmin.Media.js + ('/static/project/admin_override/js/admin_search_placeholder_for_user.js',)

	readonly_fields = ('created_at', 'get_data_dev_num', )

	# Campos que se editan
	def get_fields(self, request, obj=None):
		return (
			'created_at',
			'get_data_dev_num',
			'data_temp',
			'data_hum',
		)

	# filtros
	# Construir list_filter añadiendo uno a uno
	_list_filters = []
	_list_filters.append(FilterDataDevNum)
	list_filter = tuple(_list_filters)

	def format_col_temp_with_diff(self, temp1, temp2):
		"""Recibe dos temperaturas y devuelve: "<temp1> (<temp1 - temp2>)" con 2 decimales."""
		if temp1 is None:
			return ""
		if temp2 is None:
			return float(temp1)
		try:
			t1 = float(temp1)
			t2 = float(temp2)
			diff = t1 - t2
		except Exception:
			# Si no se pueden convertir a float, mostrar la expresión original
			return f"{temp1} ({temp1}-{temp2})"
		return format_html(f"{t1:.2f}<br>({diff:.2f})")

	def get_data_temp(self, obj):
		"""Muestra data_temp junto con la diferencia respecto a data_temp_depdown."""
		return self.format_col_temp_with_diff(obj.data_temp, obj.data_temp_depdown)
	get_data_temp.short_description = 'data_temp'
	get_data_temp.admin_order_field = 'data_temp'

	# Campos que se muestran
	def get_list_display(self, request):

		_list_display = []
		_list_display.extend([
			'pk',
			'created_at',
			'get_data_dev_num',
			'data_temp', 'data_hum',
		])
		return tuple(_list_display)


	# def has_view_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "view_inputdatahistory", obj)


	# def has_add_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "add_inputdatahistory", obj)


	# def has_change_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "change_inputdatahistory", obj)


	# def has_delete_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "delete_inputdatahistory", obj)

	def get_data_dev_num(self, obj):
		"""Muestra data_dev_num formateado."""
		return get_dev_num_str(obj.data_dev_num)
	get_data_dev_num.short_description = 'data_dev_num'
	get_data_dev_num.admin_order_field = 'data_dev_num'

	def get_data_dev_num_description(self):
		return "Número de dispositivo"

	def get_data_temp_description(self):
		return "Calle temp"

	def get_data_hum_description(self):
		return "Calle humidity"

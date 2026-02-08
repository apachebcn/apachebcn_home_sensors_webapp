# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib import admin
from .models import InputDataHistory
from rangefilter.filters import DateRangeFilter
from django.utils.html import format_html

from apps.common_functions import get_realuser_is_superuser
from apps.custom_admin import CustomAdmin
# from .admin_filters import \
# 	FilterCmsPageId, \
# 	FilterRelayErrors, \
# 	FilterDataColector1, \
# 	FilterDataColector2, \
# 	FilterDataColector3, \
# 	FilterDataDepUpFilter, \
# 	FilterDataDepDownFilter, \
# 	FilterDataAirFilter, \
# 	FilterPump1, \
# 	FilterRelayPump1, \
# 	FilterPump2, \
# 	FilterRelayPump2, \
# 	FilterPump3, \
# 	FilterRelayPump3, \
# 	FilterRelayCol1Higher, \
# 	FilterRelayCol1Lower, \
# 	FilterRelayCol2Higher, \
# 	FilterRelayCol2Lower, \
# 	FilterRelayCol3Higher, \
# 	FilterRelayCol3Lower, \
# 	FilterRelayDepUpHigher, \
# 	FilterRelayDepUpLower, \
# 	FilterRelayDepDownHigher


@admin.register(InputDataHistory)
class InputDataHistoryAdmin(CustomAdmin):

	class Media:
		js = CustomAdmin.Media.js + ('/static/project/admin_override/js/admin_search_placeholder_for_user.js',)

	readonly_fields = ('created_at', )

	# Campos que se editan
	fields = []

	def get_pro_mode(self, obj):
		if not obj.userprofile:
			return "-"
		return obj.userprofile.license_access_enable

	# filtros
	# Construir list_filter añadiendo uno a uno
	#_list_filters = []
	#_list_filters.append(FilterCmsPageId)
	#_list_filters.append(('created_at', DateRangeFilter))
	#_list_filters.append(FilterRelayErrors)
	#_list_filters.append(FilterDataColector1)
	#_list_filters.append(FilterDataColector2)
	#_list_filters.append(FilterDataColector3)
	#_list_filters.append(FilterDataDepUpFilter)
	#_list_filters.append(FilterDataDepDownFilter)
	#_list_filters.append(FilterDataAirFilter)
	#_list_filters.append(FilterPump1)
	#_list_filters.append(FilterPump2)
	#_list_filters.append(FilterPump3)
	#_list_filters.append(FilterRelayPump1)
	#_list_filters.append(FilterRelayPump2)
	#_list_filters.append(FilterRelayPump3)
	#_list_filters.append(FilterRelayCol1Higher)
	#_list_filters.append(FilterRelayCol1Lower)
	#_list_filters.append(FilterRelayCol2Higher)
	#_list_filters.append(FilterRelayCol2Lower)
	#_list_filters.append(FilterRelayCol3Higher)
	#_list_filters.append(FilterRelayCol3Lower)
	#_list_filters.append(FilterRelayDepUpHigher)
	#_list_filters.append(FilterRelayDepUpLower)
	#_list_filters.append(FilterRelayDepDownHigher)
	#list_filter = tuple(_list_filters)

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

	def get_data_s1_temp(self, obj):
		"""Muestra data_s1_temp junto con la diferencia respecto a data_temp_depdown."""
		return self.format_col_temp_with_diff(obj.data_s1_temp, obj.data_temp_depdown)
	get_data_s1_temp.short_description = 'data_s1_temp'
	get_data_s1_temp.admin_order_field = 'data_s1_temp'

	# Campos que se muestran
	def get_list_display(self, request):

		_list_display = []
		if get_realuser_is_superuser(request):
			_list_display.append('pk')
			_list_display.append('user_id')

		_list_display.extend([
			'created_at',

			'data_s1_temp',
			'data_s1_hum',

			'data_s2_temp',
			'data_s2_hum',

			'data_s3_temp',
			'data_s3_hum',

			'data_s4_temp',
			'data_s4_hum',

		])
		return tuple(_list_display)

	# Campos que va a usar cuando usamos el search
	def get_search_fields(self, request):
		if get_realuser_is_superuser(request):
			return ('user_id__username',)
		return ()  # Devuelve un tupla vacía para usuarios normales


	# def has_view_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "view_inputdatahistory", obj)


	# def has_add_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "add_inputdatahistory", obj)


	# def has_change_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "change_inputdatahistory", obj)


	# def has_delete_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputDataHistory, "delete_inputdatahistory", obj)



	def get_data_s1_temp_description(self):
		return "Calle temp"

	def get_data_s1_hum_description(self):
		return "Calle humidity"

	def get_data_s2_temp_description(self):
		return "Dormitorio matrimonio temp"

	def get_data_s2_hum_description(self):
		return "Dormitorio matrimonio humidity"

	def get_data_s3_temp_description(self):
		return "Oficina temp"

	def get_data_s3_hum_description(self):
		return "Oficina humidity"

	def get_data_s4_temp_description(self):
		return "Wc Arriba temp"

	def get_data_s4_hum_description(self):
		return "Wc Arriba humidity"

# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib import admin
from .models import InputData

from apps.common_functions import get_dev_num_str
from apps.custom_admin import CustomAdmin
from .admin_filters import FilterDataDevNum


@admin.register(InputData)
class InputDataAdmin(CustomAdmin):

	class Media:
		js = CustomAdmin.Media.js + ('/static/project/admin_override/js/admin_search_placeholder_for_user.js',)

	readonly_fields = ('updated_at', 'room_id', 'get_room_id', 'room_version', )

	# Campos que se editan
	def get_fields(self, request, obj=None):
		return (
			'updated_at',
			'get_room_id',
			'room_version',
			'room_mark_to_update',
			'room_data_temp',
			'room_data_hum'
		)

	# filtros
	# Construir list_filter añadiendo uno a uno
	_list_filters = []
	_list_filters.append(FilterDataDevNum)
	list_filter = tuple(_list_filters)

	# Campos que se muestran
	def get_list_display(self, request):
		_list_display = []
		_list_display.extend([
			'pk',
			'updated_at',
			'get_room_id',
			'room_version',
			'room_mark_to_update',
			'room_data_temp',
			'room_data_hum',
			'room_data_temp_min', 'room_data_temp_max',
			'room_data_hum_min', 'room_data_hum_max',
		])
		return _list_display


	# def has_view_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputData, "view_inputdata", obj)

	def get_room_id_description(self):
		return "Número de dispositivo"

	def get_data_temp_description(self):
		return "Temperatura"

	def get_data_hum_description(self):
		return "Humedad"

	def get_room_id(self, obj):
		"""Muestra room_id formateado."""
		return get_dev_num_str(obj.room_id)
	get_room_id.short_description = 'room_id'
	get_room_id.admin_order_field = 'room_id'
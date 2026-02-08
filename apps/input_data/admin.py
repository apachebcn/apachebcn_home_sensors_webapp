# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib import admin
from .models import InputData

from apps.common_functions import get_realuser_is_superuser
from apps.custom_admin import CustomAdmin


@admin.register(InputData)
class InputDataAdmin(CustomAdmin):

	class Media:
		js = CustomAdmin.Media.js + ('/static/project/admin_override/js/admin_search_placeholder_for_user.js',)

	readonly_fields = ('updated_at', 'data_dev_num', )

	# Campos que se editan
	def get_fields(self, request, obj=None):
		return (
			'updated_at',
			'data_dev_num',
			'data_temp', 'data_temp_min', 'data_temp_max',
			'data_hum', 'data_hum_min', 'data_hum_max',
		)

	# Campos que se muestran
	def get_list_display(self, request):

		_list_display = []
		if get_realuser_is_superuser(request):
			_list_display.append('pk')
			_list_display.append('user_id')

		_list_display.extend([
			'updated_at',
			'data_from_thermostate_local_ip',
			'data_from_thermostate_public_ip',
			'data_dev_num',
			'data_temp', 'data_temp_min', 'data_temp_max',
			'data_hum', 'data_hum_min', 'data_hum_max',
		])
		return _list_display

	# Campos que va a usar cuando usamos el search
	def get_search_fields(self, request):
		if get_realuser_is_superuser(request):
			return ('user_id__username',)
		else:
			return ()

	# def has_view_permission(self, request, obj=None):
	# 	return admin_has_permission(request, InputData, "view_inputdata", obj)

	def get_data_dev_num_description(self):
		return "Número de dispositivo"

	def get_data_temp_description(self):
		return "Temperatura"

	def get_data_hum_description(self):
		return "Humedad"

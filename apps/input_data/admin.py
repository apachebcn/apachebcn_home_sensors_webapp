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

	readonly_fields = ('created_at', 'updated_at',)

	# Campos que se editan
	def get_fields(self, request, obj=None):
		if get_realuser_is_superuser(request):
			return super().get_fields(request, obj=obj)
		else:
			return (
				'updated_at',

				'data_s1_temp', 'data_s1_temp_min', 'data_s1_temp_max',
				'data_s1_hum', 'data_s1_hum_min', 'data_s1_hum_max',
				'data_s1_updated_at',

				'data_s2_temp', 'data_s2_temp_min', 'data_s2_temp_max',
				'data_s2_hum', 'data_s2_hum_min', 'data_s2_hum_max',
				'data_s2_updated_at',

				'data_s3_temp', 'data_s3_temp_min', 'data_s3_temp_max',
				'data_s3_hum', 'data_s3_hum_min', 'data_s3_hum_max',
				'data_s3_updated_at',

				'data_s4_temp', 'data_s4_temp_min', 'data_s4_temp_max',
				'data_s4_hum', 'data_s4_hum_min', 'data_s4_hum_max',
				'data_s4_updated_at',
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

			'data_s1_temp', 'data_s1_temp_min', 'data_s1_temp_max',
			'data_s1_hum', 'data_s1_hum_min', 'data_s1_hum_max',
			'data_s1_updated_at',

			'data_s2_temp', 'data_s2_temp_min', 'data_s2_temp_max',
			'data_s2_hum', 'data_s2_hum_min', 'data_s2_hum_max',
			'data_s2_updated_at',

			'data_s3_temp', 'data_s3_temp_min', 'data_s3_temp_max',
			'data_s3_hum', 'data_s3_hum_min', 'data_s3_hum_max',
			'data_s3_updated_at',

			'data_s4_temp', 'data_s4_temp_min', 'data_s4_temp_max',
			'data_s4_hum', 'data_s4_hum_min', 'data_s4_hum_max',
			'data_s4_updated_at',
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

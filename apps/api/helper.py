# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.http import JsonResponse
from apps.decorators import apikey_required
import json

from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied

from django.utils import timezone
from apps.common_functions import is_bool, is_int, is_float, get_user_admin
from django.utils.timezone import localtime
from datetime import timedelta

from apps.input_data.models import InputData
from apps.input_data_history.models import InputDataHistory
from apps.input_data_history.helper import get_json_sensors_graph
from apps.common_functions import test_is_numeric
from project.settings import MODE

from apps.common_functions import responseToThermostate

import logging
logger = logging.getLogger('django')


@apikey_required()
def api_get_json_sensors_temp_graph(request):

	"""
	Es llamado por javascript desde la vista graph_history.html
	"""
	return get_json_sensors_graph(request, data_variable="data_temp")


@apikey_required()
def api_get_json_sensors_hum_graph(request):

	"""
	Es llamado por javascript desde la vista graph_history.html
	"""
	return get_json_sensors_graph(request, data_variable="data_hum")


@apikey_required()
def insert_input_data(request):

	"""
		Esta función la usa como api el termostato
		Envía aquí su url, y hacemos lo siguiente:
			- Almacenamos los datos de sus parametros, que son los valores de sensores y relés como entrada
			- Registramos los datos como histórico
			- Respondemos con los datos del modelo RemoteConfig, que son los valores de fuerces de reles que el usuario quiere comandar desde aquí

	Ejemplo de input:
		https://sensors.pedroreinarojas.com/api/write_data/?apikey=APIKEY_PASS&ip=127.0.0.5&room=1&temp=12&hum=22
	RESPUESTAS QUE SE ENVIARÁN AL TERMOSTATO:
		WEBAPP_OK
		WEBAPP_GET_CONFIG_FROM_THERMOSTATE
		WEBAPP_SET_CONFIG_TO_THERMOSTATE
		WEBAPP_UPDATE
		error
	"""

	from apps.global_config import LIMIT_API_INPUT_SECONDS

	def parse_int(value):
		if value is None or value == "DISABLED" or not is_int(value):
			return 0
		return int(value) if value is not None and is_int(value) else 0

	def parse_float(value):
		if value is None or value == "DISABLED" or not is_float(value):
			return 0
		return float(value)

	def parse_bool(value):
		if value is None or value == "DISABLED" or not is_bool(value):
			return 0
		if (value == "0"):
			return False
		if (value == "1"):
			return True
		return bool(value)

	def set_max_value(row, field_name):

		field_name_max = field_name + "_max"
		actual_value = getattr(row, field_name, 0)
		if not test_is_numeric(actual_value):
			return
		max_value = getattr(row, field_name_max, 0)
		if max_value:
			max_value = parse_float(max_value)
		actual_value = parse_float(actual_value)
		if max_value is None or actual_value > max_value:
			setattr(row, field_name_max, actual_value)
		return

	def set_min_value(row, field_name):

		field_name_min = field_name + "_min"
		actual_value = getattr(row, field_name, 0)
		if not test_is_numeric(actual_value):
			return
		min_value = getattr(row, field_name_min, 0)
		if min_value:
			min_value = parse_float(min_value)
		actual_value = parse_float(actual_value)
		if min_value is None or actual_value < min_value:
			setattr(row, field_name_min, actual_value)
		return

	user_ip = request.META.get('REMOTE_ADDR', 'unknown')

	if request.method != 'GET':
		message = "Bad protocol"
		logger.warning(user_ip + ": " + message)
		result = "error"
		return responseToThermostate(request, result = result, message = message)

	user_apikey = get_user_admin()
	if not user_apikey or user_apikey is None:
		raise PermissionDenied("admin user not found")


	room = request.GET.get('room', None)
	logger.info(f"RECIBIENDO DATOS del sensor room {room} con IP {user_ip}")

	data_from_thermostate_local_ip = request.GET.get('ip', None)
	data_from_thermostate_public_ip = request.META.get('REMOTE_ADDR', 'unknown')

	field_values = {}

	try:
		room = int(room)
	except Exception as e:
		message = str(e)
		result = "error"
		return responseToThermostate(request, result = result, message = message)

	if room is None or not is_int(room):
		message = "El parámetro 'room' es obligatorio y ha de ser un número entero"
		result = "error"
		return responseToThermostate(request, result = result, message = message)

	field_values["data_dev_num"] = room
	field_values["data_temp"] = request.GET.get('temp', None)
	field_values["data_hum"] = request.GET.get('hum', None)

	input_data_row = InputData.objects.filter(data_dev_num=room).first()

	if not input_data_row:
		input_data_row = InputData.objects.create(
			data_dev_num = room,
			data_temp = field_values["data_temp"],
			data_hum = field_values["data_hum"],
			data_from_thermostate_local_ip = data_from_thermostate_local_ip,
			data_from_thermostate_public_ip = data_from_thermostate_public_ip,
		)
	else:
		input_data_row.data_dev_num = room
		input_data_row.data_temp = field_values["data_temp"]
		input_data_row.data_hum = field_values["data_hum"]
		input_data_row.data_from_thermostate_local_ip = data_from_thermostate_local_ip
		input_data_row.data_from_thermostate_public_ip = data_from_thermostate_public_ip
		input_data_row.save()

	set_min_value(input_data_row, 'data_temp')
	set_max_value(input_data_row, 'data_temp')

	set_min_value(input_data_row, 'data_hum')
	set_max_value(input_data_row, 'data_hum')

	input_data_row.save()

	history_data = {
		"data_dev_num": parse_int(input_data_row.data_dev_num),
		"data_temp": parse_float(input_data_row.data_temp),
		"data_hum": parse_float(input_data_row.data_hum),
	}

	# Remover segundos y microsegundos
	def strip_seconds(dt):
		return localtime(dt).replace(second=0, microsecond=0)

	created_at = timezone.now()

	# Obtener la versión truncada de created_at
	created_at_trimmed = strip_seconds(created_at)

	# Intentar encontrar un registro con el mismo data_dev_num y created_at (sin segundos)
	obj, created = InputDataHistory.objects.update_or_create(
		data_dev_num=input_data_row.data_dev_num,
		created_at__gte=created_at_trimmed,  # Buscar registros en el mismo minuto
		created_at__lt=created_at_trimmed + timedelta(minutes=1),  # Evita valores de otros minutos
		defaults=history_data  # Datos a actualizar si ya existe
	)

	result = "WEBAPP_OK"
	return responseToThermostate(request, result = result)

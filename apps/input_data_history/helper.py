# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import timedelta
import time
import pandas as pd

from apps.common_functions import responseToThermostate, get_system_timezone
from apps.common_functions_dates import convert_local_datetime_str_to_utc
from apps.input_data_history.models import InputDataHistory

import logging
logger = logging.getLogger('django')


def convert_bool_to_js_value(value):

	if value is None:
		return None
	if value:
		return 1
	else:
		return 0


def convert_str_to_js_value(value):

	if value is None:
		return None
	return value


def get_time_difference(start_date, end_date):

	# Calcular la diferencia de tiempo
	time_difference = end_date - start_date

	# Obtener la diferencia en segundos
	seconds_difference = time_difference.total_seconds()

	# Retornar la diferencia de tiempo en segundos
	return seconds_difference


def get_history_sensors_graph_data(request, data_variable, start_local_date_str, end_local_date_str):

	# Convertir las cadenas de fecha, a fecha UTC
	utc_start_date = convert_local_datetime_str_to_utc(request, start_local_date_str)
	utc_end_date = convert_local_datetime_str_to_utc(request, end_local_date_str)

	seconds_difference = get_time_difference(utc_start_date, utc_end_date)
	minuts_difference = seconds_difference / 60
	hours_difference = minuts_difference / 60
	days_difference = hours_difference / 24
	if days_difference <= 2:  # 2 días o inferior
		"""
			2 días o inferior
		"""
		GroupId = 1
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # minuto
		resample_time_value = 1
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 4:  # 4 días o inferior
		"""
			4 días o inferior
		"""
		GroupId = 2
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # minuto
		resample_time_value = 5
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 7:
		"""
			1 semana o inferior
		"""
		GroupId = 3
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # minuto
		resample_time_value = 20
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 30:
		"""
			1 mes o inferior
		"""
		GroupId = 4
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # hora
		resample_time_value = 30
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 60:
		"""
			2 meses o inferior
		"""
		GroupId = 5
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'D'  # día
		resample_time_value = 1
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 365:
		"""
			1 año o inferior
		"""
		GroupId = 6
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'D'  # día
		resample_time_value = 1
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= (365 * 5):
		"""
			5 años o inferior
		"""
		GroupId = 7
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'W'  # semana
		resample_time_value = 1
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	else:
		"""
			Resto
		"""
		GroupId = 8
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'MS'  # Mes (1er día)
		resample_time_value = 1
		len_rows, elapsed_time_ms, data = get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)

	log_msg = f"get_history_sensors_graph_data: [G{GroupId}] FROM UTC:'{utc_start_date}' TO UTC:'{utc_end_date}'. resample='{resample_time_name}/{resample_time_value}'"

	if not data:
		logger.info(f"{log_msg} -> NO DATA")
		return False, []

	logger.info(f"{log_msg} -> Data: '{len_rows} rows', Time: '{elapsed_time_ms:.2f}ms'")

	index_time = 'created_at'

	# Preparar los resultados
	ids = []
	dates = []
	room_id = []
	values = []

	for entry in data:
		# Saltear solo si no hay timestamp válido
		if (index_time not in entry or entry[index_time] is None):
			continue

		local_start = entry[index_time]
		ids.append(convert_str_to_js_value(entry.get('id', None)))
		dates.append(local_start.strftime('%Y-%m-%d %H:%M:%S'))
		# Forzar siempre texto para room_id
		val = entry.get('room_id', None)
		if val is not None:
			# Si es float terminado en .0 o int, convertir a int primero
			try:
				if isinstance(val, float) and val.is_integer():
					val = int(val)
				elif isinstance(val, int):
					val = int(val)
			except Exception:
				pass
			val = str(val)
		if val is not None:
			room_id.append(val)
		else:
			room_id.append("")
		# Solo un valor, depende de data_variable
		values.append(convert_str_to_js_value(entry.get(data_variable, None)))

	plot_data = {}
	plot_data['id'] = ids
	plot_data['dates'] = dates
	plot_data['room_id'] = room_id
	plot_data['value'] = values

	return plot_data


def get_json_sensors_graph(request, data_variable):

	from datetime import datetime
	from django.http import JsonResponse
	from apps.common_functions_dates import get_GET_or_POST_start_datetime_str
	from apps.common_functions_dates import get_GET_or_POST_end_datetime_str
	from apps.common_functions import get_dev_num_str

	def convert_timestamp(timestamp):  # Para pruebas, para ver el timestamp en formato legible
		# Si el timestamp está en milisegundos, lo convertimos a segundos
		if timestamp > 1000000000000:
			timestamp = timestamp / 1000
		# Convertir el timestamp a un objeto datetime
		dt = datetime.fromtimestamp(timestamp)
		# Formatear la fecha y hora de forma legible
		value = dt.strftime('%Y-%m-%d %H:%M:%S')
		return value

	start_local_date_str = get_GET_or_POST_start_datetime_str(request, None)
	if start_local_date_str is None:
		return responseToThermostate(request, result = "error", message = "error: " + _("Fecha Inicio no puede ser nulo"))
	end_local_date_str = get_GET_or_POST_end_datetime_str(request, None)
	if end_local_date_str is None:
		return responseToThermostate(request, result = "error", message = "error: " + _("Fecha Fin no puede ser nulo"))
	if start_local_date_str > end_local_date_str:
		return responseToThermostate(request, result = "error", message = "error: " + _("Fecha Fin no puede ser inferior a Fecha Inicio"))

	try:
		plot_data = get_history_sensors_graph_data(request, data_variable, start_local_date_str, end_local_date_str)
	except Exception as e:
		logger.error(str(e))
		return JsonResponse({'status': 'error', 'error': f"get_json_sensors_graph : {e}"})

	if not plot_data:
		utc_start_date = convert_local_datetime_str_to_utc(request, start_local_date_str)
		utc_end_date = convert_local_datetime_str_to_utc(request, end_local_date_str)
		msg = f"NO DATA FOR\n USER: '{request.user}'\nFROM UTC:'{utc_start_date}'\nTO UTC:'{utc_end_date}'"
		return JsonResponse({'status': 'error', 'error': msg})


	# Agrupar por room_id, usando plot_data['value'] como y
	from collections import defaultdict
	series_dict = defaultdict(list)
	for i in range(len(plot_data['dates'])):
		date_str = plot_data['dates'][i]
		datetime_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
		timestamp = datetime_obj.timestamp() * 1000  # Highcharts espera ms
		room_id = plot_data['room_id'][i] if 'room_id' in plot_data else None
		# Etiqueta legible usando función centralizada
		try:
			dev_label = get_dev_num_str(int(float(room_id)))
		except Exception:
			dev_label = str(room_id)
		y_value = plot_data['value'][i] if 'value' in plot_data else None
		if y_value is not None:
			series_dict[dev_label].append([timestamp, y_value])

	series_data = []
	for dev_label, points in series_dict.items():
		series_data.append({
			"name": dev_label,
			"object_name": dev_label,
			"yAxis": 1,
			"data": points
		})

	info_dict = {
		"start_local_date": start_local_date_str,
		"end_local_date": end_local_date_str,
	}

	return JsonResponse({
		"info": info_dict,
		"data": series_data
	})


def convert_data_created_date_to_local(request, data):

	user_timezone = get_system_timezone()  # Obtener la zona horaria del usuario
	# Iterar sobre la lista de diccionarios y actualizar el campo 'created_at'
	for item in data:
		original_time = item['created_at']
		# Convertir el campo 'created_at' a la zona horaria local
		localized_time = timezone.localtime(original_time, timezone=user_timezone)
		item['created_at'] = localized_time
	return


def get_sensors_rows(request, data_variable, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value):

	import json
	import base64
	from project.settings import cache_enable

	start_time = time.time()

	data = InputDataHistory.objects.filter(
		created_at__gte=utc_start_date,
		created_at__lte=utc_end_date
	).order_by('created_at')

	if not data:
		return 0, 0, []

	fields = [
		'id',
		'created_at',
		'room_id',
	]
	fields.append(data_variable)
	data = data.values(*fields)

	if not data:
		return 0, 0, []

	convert_data_created_date_to_local(request, data)

	# Logger para verificar datos originales
	# (log eliminado: user_selected_profile)

	# Convertir a DataFrame
	df = pd.DataFrame(list(data))

	# Convertir la columna 'created_at' a objetos datetime
	df['created_at'] = pd.to_datetime(df['created_at'])

	# Establecer 'created_at' como índice
	df.set_index('created_at', inplace=True)

	# Logger para verificar DataFrame
	# (log eliminado: user_selected_profile)

	if days_difference <= 2:
		# Guardar último id antes del resample
		last_row = df.iloc[[-1]].copy()
		last_row['id'] = last_row['id'].astype(int)
		last_row = last_row.reset_index()

	# REINDEXADO CON FRECUENCIA DINÁMICA PARA RELLENAR HUECOS
	# Primero hacer resample de los datos originales
	freq_str = f'{resample_time_value}{resample_time_name}'
	# Solo promediar la columna de datos, no room_id
	agg_dict = {data_variable: 'mean'}
	if 'id' in df.columns:
		agg_dict['id'] = 'first'
	if 'room_id' in df.columns:
		agg_dict['room_id'] = 'first'
	df_resampled = df.resample(freq_str).agg(agg_dict)

	# siempre con los huecos
	data = df_resampled.reset_index()

	# Añadir la última fila al final si no está ya incluida
	if days_difference <= 2:
		if last_row['id'].iloc[0] != data['id'].iloc[-1]:
			data = pd.concat([data, last_row], ignore_index=False)

	# Redondear los valores flotantes a 2 decimales (solo los que no son NaN)
	float_columns = [
		data_variable
	]
	data[float_columns] = data[float_columns].round(2)

	# NO eliminar filas donde 'id' es NaN - mantener huecos para Highcharts
	# Solo forzar id a entero donde no es NaN
	data.loc[data['id'].notna(), 'id'] = data.loc[data['id'].notna(), 'id'].astype(int)

	# Convertir NaN a None para JSON serialization, manteniendo estructura de huecos
	data = data.astype(object).where(pd.notnull(data), None)

	# Convertir los datos de nuevo a una lista de diccionarios
	data_list = data.to_dict('records')

	# Logger temporal para verificar reindexado
	# logger.info(f"REINDEXED CHECK: user={request.user}, freq={freq_str}, total={len(data_list)}")
	# for i, entry in enumerate(data_list[:5]):  # Solo primeros 5
	# 	timestamp = entry.get('created_at', 'N/A')
	# 	temp = entry.get('room_data_temp', 'NULL')
	# 	id_val = entry.get('id', 'NULL')
	# 	logger.info(f"  [{i}] {timestamp} -> temp={temp}, id={id_val}")

	end_time = time.time()
	elapsed_time_ms = (end_time - start_time) * 1000

	return len(data), elapsed_time_ms, data_list

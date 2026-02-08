# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.utils.translation import gettext as _
from django.utils import timezone
from datetime import timedelta
import time
import pandas as pd

from apps.common_functions import responseToThermostate
from apps.common_functions_dates import convert_local_datetime_str_to_utc
from apps.input_data_history.models import InputDataHistory

import logging
logger = logging.getLogger('django')


def get_sensors_data_list_all_names(request):

	names = [
		"id",
		"data_s1_temp",
		"data_s1_hum",
		"data_s2_temp",
		"data_s2_hum",
		"data_s3_temp",
		"data_s3_hum",
		"data_s4_temp",
		"data_s4_hum",
	]
	return names


def in_available_list_names(list_available_names, name):
	if name in list_available_names:
		if list_available_names[name]:
			return True
		else:
			return False
	return False


def get_sensors_data_available_names(request):

	names = get_sensors_data_list_all_names(request)
	return names


def get_sensors_data_available_titles(request):

	titles = {}
	names = get_sensors_data_available_names(request)
	for name in names:
		title = name + "_title"
		titles[name] = title
	return titles


def get_sensors_data_list_availables(request):

	availables = {}
	names = get_sensors_data_list_all_names(request)
	for name in names:
		if name[:11] != "data_relay_":
			availables[name] = True
			continue
		available = name + "_available"
		if available:
			availables[name] = True
		else:
			availables[name] = False
	return availables


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


def get_history_data_graph_data(request, thermostate_data_fields_availables, start_local_date_str, end_local_date_str):

	realtime = request.GET.get('realtime', False)

	# Convertir las cadenas de fecha, a fecha UTC
	utc_start_date = convert_local_datetime_str_to_utc(request, start_local_date_str)
	utc_end_date = convert_local_datetime_str_to_utc(request, end_local_date_str)

	seconds_difference = get_time_difference(utc_start_date, utc_end_date)
	minuts_difference = seconds_difference / 60
	hours_difference = minuts_difference / 60
	days_difference = hours_difference / 24
	if realtime:
		"""
			realtime
		"""
		GroupId = 1
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # minuto
		resample_time_value = 1
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 2:  # 2 días o inferior
		"""
			2 días o inferior
		"""
		GroupId = 1
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # minuto
		resample_time_value = 1
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 4:  # 4 días o inferior
		"""
			4 días o inferior
		"""
		GroupId = 2
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # minuto
		resample_time_value = 5
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 7:
		"""
			1 semana o inferior
		"""
		GroupId = 3
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # minuto
		resample_time_value = 20
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 30:
		"""
			1 mes o inferior
		"""
		GroupId = 4
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'min'  # hora
		resample_time_value = 30
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 60:
		"""
			2 meses o inferior
		"""
		GroupId = 5
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'D'  # día
		resample_time_value = 1
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= 365:
		"""
			1 año o inferior
		"""
		GroupId = 6
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'D'  # día
		resample_time_value = 1
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	elif days_difference <= (365 * 5):
		"""
			5 años o inferior
		"""
		GroupId = 7
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'W'  # semana
		resample_time_value = 1
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)
	else:
		"""
			Resto
		"""
		GroupId = 8
		utc_start_date = utc_start_date
		utc_end_date = utc_end_date
		resample_time_name = 'MS'  # Mes (1er día)
		resample_time_value = 1
		result_from_cache, len_rows, elapsed_time_ms, data = get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value)

	log_msg = f"get_history_data_graph_data: [G{GroupId}] for user '{request.user_selected}'. FROM UTC:'{utc_start_date}' TO UTC:'{utc_end_date}'. resample='{resample_time_name}/{resample_time_value}'"

	if not data:
		if request.user_selected_profile.log_to_console:
			logger.info(f"{log_msg} -> NO DATA")
		return False, []

	if request.user_selected_profile.log_to_console:
		logger.info(f"{log_msg} -> Data: '{len_rows_formatted} rows', Time: '{elapsed_time_ms:.2f}ms'")

	index_time = 'created_at'

	# Preparar los resultados
	ids = []
	dates = []
	data_s1_temp = []
	data_s1_hum = []
	data_s2_temp = []
	data_s2_hum = []
	data_s3_temp = []
	data_s3_hum = []
	data_s4_temp = []
	data_s4_hum = []

	for entry in data:

		# Saltear solo si no hay timestamp válido
		if (index_time not in entry or entry[index_time] is None):
			continue

		# local_start = entry[index_time].astimezone(None)
		local_start = entry[index_time]
		ids.append(convert_str_to_js_value(entry.get('id', None)))
		dates.append(local_start.strftime('%Y-%m-%d %H:%M:%S'))
		data_s1_temp.append(convert_str_to_js_value(entry.get('data_s1_temp', None)))
		data_s1_hum.append(convert_str_to_js_value(entry.get('data_s1_hum', None)))
		data_s2_temp.append(convert_str_to_js_value(entry.get('data_s2_temp', None)))
		data_s2_hum.append(convert_str_to_js_value(entry.get('data_s2_hum', None)))
		data_s3_temp.append(convert_str_to_js_value(entry.get('data_s3_temp', None)))
		data_s3_hum.append(convert_str_to_js_value(entry.get('data_s3_hum', None)))
		data_s4_temp.append(convert_str_to_js_value(entry.get('data_s4_temp', None)))
		data_s4_hum.append(convert_str_to_js_value(entry.get('data_s4_hum', None)))
	plot_data['id'] = ids
	plot_data['dates'] = dates
	plot_data['data_s1_temp'] = data_s1_temp
	plot_data['data_s1_hum'] = data_s1_hum
	plot_data['data_s2_temp'] = data_s2_temp
	plot_data['data_s2_hum'] = data_s2_hum
	plot_data['data_s3_temp'] = data_s3_temp
	plot_data['data_s3_hum'] = data_s3_hum
	plot_data['data_s4_temp'] = data_s4_temp
	plot_data['data_s4_hum'] = data_s4_hum

	return result_from_cache, plot_data


def get_json_data_graph(request):

	from django.http import JsonResponse
	from apps.common_functions_dates import get_GET_or_POST_start_datetime_str
	from apps.common_functions_dates import get_GET_or_POST_end_datetime_str
	import pytz
	from datetime import datetime

	def convert_timestamp(timestamp):  # Para pruebas, para ver el timestamp en formato legible
		# Si el timestamp está en milisegundos, lo convertimos a segundos
		if timestamp > 1000000000000:
			timestamp = timestamp / 1000
		# Convertir el timestamp a un objeto datetime
		dt = datetime.fromtimestamp(timestamp)
		# Formatear la fecha y hora de forma legible
		value = dt.strftime('%Y-%m-%d %H:%M:%S')
		return value

	realtime = request.GET.get('realtime', False)
	if realtime:
		user_timezone = request.user_timezone
		user_otion = request.user_selected_option
		last_minutes = int(getattr(user_otion, "graph_time_real_last_minutes", 60))
		now_utc = datetime.now(pytz.UTC)  # Obtener la hora en UTC
		now_local = now_utc.astimezone(user_timezone)  # Convertir a la zona horaria del usuario
		start_local_date_str = str(now_local - timedelta(minutes=last_minutes))
		end_local_date_str = str(now_local)
	else:
		start_local_date_str = get_GET_or_POST_start_datetime_str(request, None)
		if start_local_date_str is None:
			return responseToThermostate(request, result = "error", message = "error: " + _("Fecha Inicio no puede ser nulo"))
		end_local_date_str = get_GET_or_POST_end_datetime_str(request, None)
		if end_local_date_str is None:
			return responseToThermostate(request, result = "error", message = "error: " + _("Fecha Fin no puede ser nulo"))
		if start_local_date_str > end_local_date_str:
			return responseToThermostate(request, result = "error", message = "error: " + _("Fecha Fin no puede ser inferior a Fecha Inicio"))

	names = get_sensors_data_available_names(request)
	titles = get_sensors_data_available_titles(request)
	availables = get_sensors_data_list_availables(request)
	total_availables = sum(availables.values())
	if total_availables < 1:
		return JsonResponse({'status': 'error', 'error': _("No hay ningún campo disponible seleccionado")})

	try:
		result_from_cache, plot_data = get_history_data_graph_data(request, availables, start_local_date_str, end_local_date_str)
	except Exception as e:
		logger.error(str(e))
		return JsonResponse({'status': 'error', 'error': f"get_json_data_graph_view : {e}"})

	if not plot_data:
		utc_start_date = convert_local_datetime_str_to_utc(request, start_local_date_str)
		utc_end_date = convert_local_datetime_str_to_utc(request, end_local_date_str)
		msg = f"NO DATA FOR\n USER: '{request.user_selected}'\nFROM UTC:'{utc_start_date}'\nTO UTC:'{utc_end_date}'"
		return JsonResponse({'status': 'error', 'error': msg})

	x = []
	series_data = []
	for name in names:
		values = []
		if not availables[name]:
			continue
		for i in range(len(plot_data['dates'])):
			date_str = plot_data['dates'][i]
			datetime_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
			timestamp = datetime_obj.timestamp()
			x.append(convert_timestamp(timestamp))
			if name in plot_data and len(plot_data[name]):
				value = plot_data[name][i]
			else:
				value = None
			values.append([(timestamp * 1000), value])
		if realtime:
			# Insertar ultimo point para simular tiempo real
			now_utc = datetime.now(pytz.UTC)
			if now_utc.tzinfo is None:
				now_utc = user_timezone.localize(now_utc)
			now_local = now_utc.astimezone(user_timezone)
			now_local_str = now_local.strftime('%Y-%m-%d %H:%M:%S')
			datetime_obj = datetime.strptime(now_local_str, '%Y-%m-%d %H:%M:%S')
			timestamp = datetime_obj.timestamp()
			x.append(convert_timestamp(timestamp))
			values.append([(timestamp * 1000), None])

		title = ""
		if name in titles:
			title = titles[name]
		if title == "":
			title = name

		series_data.append({
			"name": title,
			"object_name": name,
			"yAxis": 1,
			"data": values
		})

	# return JsonResponse(series_data, safe=False)

	info_dict = {
		"start_local_date": start_local_date_str,
		"end_local_date": end_local_date_str,
		"from_cache": result_from_cache
	}

	return JsonResponse({
		"info": info_dict,
		"data": series_data
	})


def convert_data_created_date_to_local(request, data):

	user_timezone = request.user_timezone  # Obtener la zona horaria del usuario
	# Iterar sobre la lista de diccionarios y actualizar el campo 'created_at'
	for item in data:
		original_time = item['created_at']
		# Convertir el campo 'created_at' a la zona horaria local
		localized_time = timezone.localtime(original_time, timezone=user_timezone)
		item['created_at'] = localized_time
	return


def get_rows(request, thermostate_data_fields_availables, days_difference, utc_start_date, utc_end_date, resample_time_name, resample_time_value):

	import json
	import base64
	from project.settings import cache_enable

	start_time = time.time()

	data = InputDataHistory.objects.filter(
		user_id=request.user_selected,
		created_at__gte=utc_start_date,
		created_at__lte=utc_end_date
	).order_by('created_at')

	if not data:
		return False, 0, 0, []

	if cache_enable:

		first_created_at = data.first().created_at
		last_created_at = data.last().created_at


	fields = [
		'id',
		'created_at',
		'data_s1_temp',
		'data_s1_hum',
		'data_s2_temp',
		'data_s2_hum',
		'data_s3_temp',
		'data_s3_hum',
		'data_s4_temp',
		'data_s4_hum',
	]
	for field in fields:
		if field[:11] == "data_relay_":
			if (not in_available_list_names(thermostate_data_fields_availables, field)):
				fields.remove(field)
	data = data.values(*fields)

	if not data:
		return False, 0, 0, []

	convert_data_created_date_to_local(request, data)

	# Logger para verificar datos originales
	if request.user_selected_profile.log_to_console:
		logger.info(f"ORIGINAL DATA: user={request.user_selected}, count={len(data)}")

	# Convertir a DataFrame
	df = pd.DataFrame(list(data))

	# Convertir la columna 'created_at' a objetos datetime
	df['created_at'] = pd.to_datetime(df['created_at'])

	# Establecer 'created_at' como índice
	df.set_index('created_at', inplace=True)

	# Logger para verificar DataFrame
	if request.user_selected_profile.log_to_console:
		logger.info(f"DATAFRAME: shape={df.shape}, index_range={df.index.min()} to {df.index.max()}")

	if days_difference <= 2:
		# Guardar último id antes del resample
		last_row = df.iloc[[-1]].copy()
		last_row['id'] = last_row['id'].astype(int)
		last_row = last_row.reset_index()

	# REINDEXADO CON FRECUENCIA DINÁMICA PARA RELLENAR HUECOS
	# Primero hacer resample de los datos originales
	freq_str = f'{resample_time_value}{resample_time_name}'
	df_resampled = df.resample(freq_str).mean()

	# siempre con los huecos
	data = df_resampled.reset_index()

	# Añadir la última fila al final si no está ya incluida
	if days_difference <= 2:
		if last_row['id'].iloc[0] != data['id'].iloc[-1]:
			data = pd.concat([data, last_row], ignore_index=False)

	# Redondear los valores flotantes a 2 decimales (solo los que no son NaN)
	float_columns = [
		'data_s1_temp',
		'data_temp_depup',
		'data_temp_depdown',
		'data_temp_air'
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
	# logger.info(f"REINDEXED CHECK: user={request.user_selected}, freq={freq_str}, total={len(data_list)}")
	# for i, entry in enumerate(data_list[:5]):  # Solo primeros 5
	# 	timestamp = entry.get('created_at', 'N/A')
	# 	temp = entry.get('data_s1_temp', 'NULL')
	# 	id_val = entry.get('id', 'NULL')
	# 	logger.info(f"  [{i}] {timestamp} -> temp={temp}, id={id_val}")

	end_time = time.time()
	elapsed_time_ms = (end_time - start_time) * 1000

	return False, len(data), elapsed_time_ms, data_list


def save_graphic_settings(request, realtime=False):

	from apps.graphic_realtime_settings.models import GraphicRealtimeSettings
	from apps.graphic_history_settings.forms import GraphicHistorySettingsForm
	from apps.graphic_history_settings.models import GraphicHistorySettings
	from apps.graphic_realtime_settings.forms import GraphicRealtimeSettingsForm

	if realtime:
		row = GraphicRealtimeSettings.objects.filter(user_id=request.user).first()
		if not row:
			return "no config row found"
		form = GraphicRealtimeSettingsForm(instance = row)
	else:
		row = GraphicHistorySettings.objects.filter(user_id=request.user).first()
		if not row:
			return "no config row found"
		form = GraphicHistorySettingsForm(instance = row)

	if request.method == 'POST':
		try:
			changes = 0
			for form_field in form.fields:
				widget = form.fields[form_field].widget
				input_type = getattr(widget, "input_type")
				value = request.POST.get(form_field, None)
				if input_type == "select":
					if "_visible" in form_field or "_fill" in form_field or "_points" in form_field:
						if value is None:
							value = False
						elif value == "1":
							value = True
						elif value == "0":
							value = False
						else:
							value = False

				if value is not None:
					# logger.info(f"{form_field} = {value} !!!")
					setattr(row, form_field, value)
					changes += 1
			if changes:
				row.save()
		except Exception as e:
			logger.error(str(e))
			return f"Exception {e}"

	return True

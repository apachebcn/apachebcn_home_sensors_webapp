# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.utils.translation import gettext as _
from dateutil import parser
import os

from apps.common_functions import get_system_timezone

import logging
logger = logging.getLogger('django')


def convert_local_datetime_str_to_utc(request, date_str):
	"""
	Convierte una cadena de fecha y hora en formato '%Y-%m-%d %H:%M:%S' a un objeto datetime consciente de la zona horaria
	local y luego a UTC.
	"""
	# convierto a naive datetime
	naive_datetime = parse_str_to_naive_datetime(date_str)

	# cojo user timezone (ZoneInfo)
	user_timezone = get_system_timezone()

	# Asigno zona horaria local usando ZoneInfo
	local_datetime = naive_datetime.replace(tzinfo=user_timezone)

	# La convierto a hora UTC que será la necesaria para la query
	from datetime import timezone as dt_timezone
	utc_datetime = local_datetime.astimezone(dt_timezone.utc)

	return utc_datetime


def get_iso_datetime_days_ago(request, days_ago):
	"""
	Devuelve la fecha y hora de inicio del día (00:00) hace 'days_ago' días en la zona horaria local.
	"""
	from datetime import timedelta
	from django.utils import timezone

	# Obtener la fecha y hora actual en UTC
	now_utc = timezone.now()

	# cojo user timezone
	user_timezone = get_system_timezone()

	# Convertir la fecha y hora actual a la zona horaria local
	now_local = now_utc.astimezone(user_timezone)

	# Restar los días pasados como argumento
	date_days_ago = now_local - timedelta(days=days_ago)

	# Ajustar la fecha y hora para comenzar en el inicio del día (00:00)
	date_days_ago = date_days_ago.replace(hour=0, minute=0, second=0, microsecond=0)

	return date_days_ago.strftime('%Y-%m-%dT%H:%M')


def get_startdatetime_of_week():

	"""
	Devuelve detetime de la fecha y hora de inicio de la semana actual (lunes a las 00:00).
	"""
	from datetime import datetime, timedelta
	today = datetime.now()
	start_of_week = today - timedelta(days=today.weekday())
	start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
	return start_of_week


def get_iso_datetime_last_week(request):

	"""
	Devuelve la fecha y hora de inicio del día (00:00) hace exactamente 7 días en la zona horaria local.
	"""
	from datetime import timedelta
	from django.utils import timezone

	# Obtener la fecha y hora actual en UTC
	now_utc = timezone.now()

	# cojo user timezone
	user_timezone = get_system_timezone()

	# Convertir la fecha y hora actual a la zona horaria local
	now_local = now_utc.astimezone(user_timezone)

	# Restar 7 días a la fecha y hora actual
	start_of_last_week = now_local - timedelta(days=7)

	# Ajustar la fecha y hora para comenzar en el inicio del día (00:00)
	start_of_last_week = start_of_last_week.replace(hour=0, minute=0, second=0, microsecond=0)

	return start_of_last_week.strftime('%Y-%m-%dT%H:%M')


def get_iso_datetime_end_of_today(request):

	from django.utils import timezone

	user_timezone = get_system_timezone()

	# Obtener la fecha y hora actual en UTC
	now_utc = timezone.now()

	# Convertir la fecha y hora a la zona horaria especificada
	today = now_utc.astimezone(user_timezone)

	# Formatear la fecha y hora en ISO 8601 (fin del día)
	return today.strftime('%Y-%m-%dT23:59')


def parse_str_to_naive_datetime(local_date_str):
	try:
		# Eliminar la 'Z' si la fecha está en formato ISO (con zona horaria UTC)
		if local_date_str.endswith('Z'):
			local_date_str = local_date_str[:-1]  # Eliminar la 'Z'

		# Intentar parsear la fecha (sin zona horaria)
		datetime_obj = parser.parse(local_date_str)

		# Si la fecha tiene una zona horaria, convertirla a naive datetime
		if datetime_obj.tzinfo is not None:
			datetime_obj = datetime_obj.replace(tzinfo=None)

		return datetime_obj

	except ValueError:
		return None


def get_GET_or_POST_start_datetime_str(request, default_value):

	get_value = False
	if request.method == 'GET':
		get_value = request.GET.get('start_local_date_str', '')
	if request.method == 'POST':
		get_value = request.POST.get('start_local_date_str', '')
	if get_value:
		return get_value
	return default_value


def get_GET_or_POST_end_datetime_str(request, default_value):

	get_value = False
	if request.method == 'GET':
		get_value = request.GET.get('end_local_date_str', '')
	if request.method == 'POST':
		get_value = request.POST.get('end_local_date_str', '')
	if get_value:
		return get_value
	return default_value


def human_readable_time(seconds):
	intervals = (
		(_('Y'), 31536000),  # 60 * 60 * 24 * 365
		(_('M'), 2592000),  # 60 * 60 * 24 * 30
		(_('D'), 86400),      # 60 * 60 * 24
		(_('H'), 3600),      # 60 * 60
		(_("'"), 60),
		(_('"'), 1),
	)
	result = []
	for name, count in intervals:
		value = seconds // count
		if value:
			seconds -= value * count
			if value == 1:
				name = name.rstrip('s')
			result.append(f"{value}{name}")

	return ' '.join(result)

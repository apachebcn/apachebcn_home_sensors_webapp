# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.html import format_html

from .helper import get_json_sensors_graph
from apps.common_functions_dates import get_GET_or_POST_start_datetime_str, get_GET_or_POST_end_datetime_str
from apps.common_functions_dates import get_iso_datetime_end_of_today
from apps.common_functions_dates import get_iso_datetime_last_week
from apps.common_functions_dates import get_iso_datetime_days_ago


import logging
logger = logging.getLogger('django')


@login_required(login_url='/form_login/')
def history_sensors_graph_temp_view(request):
	return data_graph_view(request, message_error="", data_variable="data_temp")


@login_required(login_url='/form_login/')
def history_sensors_graph_hum_view(request):
	return data_graph_view(request, message_error="", data_variable="data_hum")


"""
Es llamado por javascript desde la vista graph_history.html
"""
@login_required(login_url='/form_login/')
def get_json_sensors_graph_temp_view(request):
	return get_json_sensors_graph(request, data_variable="data_temp")


"""
Es llamado por javascript desde la vista graph_history.html
"""
@login_required(login_url='/form_login/')
def get_json_sensors_graph_hum_view(request):
	return get_json_sensors_graph(request, data_variable="data_hum")


def data_graph_view(request, message_error = "", apikey = False, data_variable = "data_temp"):

	start_local_date_str = get_GET_or_POST_start_datetime_str(request, False)
	end_local_date_str = get_GET_or_POST_end_datetime_str(request, False)
	form_showMissingData = request.GET.get('form_showMissingData', 0)
	form_showDateControls = request.GET.get('form_showDateControls', 0)

	if not start_local_date_str:
		default_days_ago = 1
		if default_days_ago < 1:
			default_days_ago = 1
		today_end = get_iso_datetime_end_of_today(request)
		week_start = str(get_iso_datetime_last_week(request))
		date_selector_graph = request.GET.get('date_selector_graph')
		if date_selector_graph:
			start_local_date_str = request.GET.get('start_local_date_str', False)
			end_local_date_str = request.GET.get('end_local_date_str', False)
		elif default_days_ago:
			start_local_date_str = str(get_iso_datetime_days_ago(request, (default_days_ago - 1)))
			end_local_date_str = str(get_GET_or_POST_end_datetime_str(request, today_end))
		else:
			start_local_date_str = str(week_start)
			end_local_date_str = str(get_GET_or_POST_end_datetime_str(request, today_end))

	if data_variable == "data_temp":
		graph_title = format_html(_("Histórico Gráfico Temperatura"))
		page_title = format_html(_("Histórico Gráfico Temperatura"))
	else:
		graph_title = format_html(_("Histórico Gráfico Humedad"))
		page_title = format_html(_("Histórico Gráfico Humedad"))

	context = {
		'title': page_title,
		'graph_title': graph_title,
		'message_error': message_error,
		'start_local_date_str': start_local_date_str,
		'end_local_date_str': end_local_date_str,
		'form_showMissingData': form_showMissingData,
		'form_showDateControls': form_showDateControls,
		'graph_tooltip_format_table': 0,
		'data_variable': data_variable,
		'form_action': "/get_json_sensors_graph_temp_view/" if data_variable == "data_temp" else "/get_json_sensors_graph_hum_view/",
	}

	return render(request, 'pages/graph_history.html', context)

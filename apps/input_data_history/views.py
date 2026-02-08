# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from urllib.parse import urljoin
from datetime import datetime
from django.utils.html import format_html

from .helper import get_json_data_graph
from .helper import get_sensors_data_available_titles
from .helper import get_sensors_data_list_availables
from .helper import save_graphic_settings
from apps.common_functions_dates import get_GET_or_POST_start_datetime_str, get_GET_or_POST_end_datetime_str
from apps.common_functions_dates import get_iso_datetime_end_of_today
from apps.common_functions_dates import get_iso_datetime_last_week
from apps.common_functions_dates import get_iso_datetime_days_ago
from apps.common_functions import get_form_post_field
from apps.common_functions import test_is_numeric
from apps.input_data_history.models import InputDataHistory
from apps.graphic_realtime_settings.models import GraphicRealtimeSettings
from apps.graphic_history_settings.forms import GraphicHistorySettingsForm
from apps.graphic_history_settings.models import GraphicHistorySettings
from apps.graphic_realtime_settings.forms import GraphicRealtimeSettingsForm


import logging
logger = logging.getLogger('django')


@login_required(login_url='/form_login/')
def history_data_graph_view(request):

	from apps.input_data_history.views import data_graph_view
	message_error = ""
	if request.POST.get("save", False):
		result = save_graphic_settings(request, realtime = False)
		if result is not True:
			message_error = result
	return data_graph_view(request, realtime=False, message_error = message_error)


@login_required(login_url='/form_login/')
def realtime_data_graph_info_view(request):

	username = str(user_selected.username)
	rows = UserApikey.objects.filter(user_id__id = user_selected.id, app_access='graph_realtime')

	base_url = f"//{request.get_host()}/"

	# Construimos las URLs completas usando el dominio actual
	list_urls = [urljoin(base_url, f"api/realtime_data_graph_view?apikey={apikey.apikey}") for apikey in rows]

	context = {
		'title': _("Tiempo real Gráfico del termostato de {}".format(username)),
		'list_urls': list_urls
	}

	return render(request, 'pages/graph_realtime_info.html', context)


"""
Es llamado por javascript desde la vista graph_history.html
"""
@login_required(login_url='/form_login/')
def get_json_data_graph_view(request):

	return get_json_data_graph(request)


def data_graph_view(request, realtime, message_error = "", apikey = False):

	useroption = request.user_selected_option
	if not useroption:
		raise Exception("Error getting user.options")

	start_local_date_str = get_GET_or_POST_start_datetime_str(request, False)
	end_local_date_str = get_GET_or_POST_end_datetime_str(request, False)
	form_showMissingData = request.GET.get('form_showMissingData', 0)
	form_showDateControls = request.GET.get('form_showDateControls', 0)

	if not realtime and not start_local_date_str:
		default_days_ago = useroption.graph_default_days_ago
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

	if realtime:
		data = GraphicRealtimeSettings.objects.filter(user_id=request.user).first()
		if not data:
			data = GraphicRealtimeSettings.objects.create(user_id = user_selected)
		form = GraphicRealtimeSettingsForm(instance = data)
	else:
		data = GraphicHistorySettings.objects.filter(user_id=request.user).first()
		if not data:
			data = GraphicHistorySettings.objects.create(user_id = user_selected)
		form = GraphicHistorySettingsForm(instance = data)

	username = str(user_selected.username)
	if realtime:
		graph_title = format_html(_("Tiempo real Gráfico del termostato de '{}'".format(username)))
		page_title = format_html(_("Tiempo real Gráfico del termostato"))
	else:
		graph_title = format_html(_("Histórico Gráfico del termostato de '{}'".format(username)))
		page_title = format_html(_("Histórico Gráfico del termostato"))
	context = {
		'title': page_title,
		'graph_title': graph_title,
		'form': form,
		'message_error': message_error,
		'username': username,
		'start_local_date_str': start_local_date_str,
		'end_local_date_str': end_local_date_str,
		'form_showMissingData': form_showMissingData,
		'form_showDateControls': form_showDateControls,
		'graph_tooltip_format_table': useroption.graph_tooltip_format_table
	}

	titles = get_sensors_data_available_titles(request)
	for title_key, title_value in titles.items():
		context[title_key + "_title"] = title_value
	availables = get_sensors_data_list_availables(request)
	for available_key, available_value in availables.items():
		context[available_key + "_available"] = available_value

	if realtime:
		context['apikey'] = apikey
		return render(request, 'pages/graph_realtime.html', context)
	else:
		return render(request, 'pages/graph_history.html', context)


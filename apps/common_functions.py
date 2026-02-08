# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial


from django.http import HttpResponse, JsonResponse

from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.template import loader
from django.contrib.auth import authenticate, login as do_login, logout as do_logout

import logging
logger = logging.getLogger('django')



import logging
logger = logging.getLogger('django')


def responseToThermostate(request, result, message = ""):

	if result:
		if message:
			return HttpResponse(f"result={result}&message={message}")
		else:
			return HttpResponse(f"result={result}")
	else:
		if message:
			return JsonResponse(
				{
					'result': "error",
					'message': message
				},
				safe=False
			)
		else:
			return JsonResponse(
				{
					'result': "error",
				},
				safe=False
			)

def test_is_numeric(numero):

	try:
		int(float(numero))
	except:
		return False
	return True


def has_error_in_dict(object):

	if isinstance(object, dict):
		if 'error' in object or 'Error' in object or 'ERROR' in object:
			return True
	return False


def test_keys_in_dict(variable_dict, keys):

	if not isinstance(variable_dict, dict):
		return False
	if not variable_dict:
		return False
	for key in keys:
		if key not in variable_dict:
			return False
	return True


def test_keys_and_values_in_dict(variable_dict, keys):

	if not isinstance(variable_dict, dict):
		return False
	if not variable_dict:
		return False
	for key in keys:
		need_value = keys[key]
		if key not in variable_dict:
			return False
		if need_value:
			value = variable_dict[key]
			if value is None or value == '':
				return False
	return True


def paginador_object_context(context, model_rows, pags_per_page, pag_sel):

	from django.core.paginator import Paginator

	if not model_rows or not len(model_rows):
		context['data'] = []
		context['total_resultados'] = 0
		context['es_paginado'] = False
		context['pagina'] = 1
		context['registros_por_pagina'] = pags_per_page
		context['paginador_ultima_pagina'] = 1
		context['paginador_atras_5'] = 0
		context['paginador_atras_4'] = 0
		context['paginador_atras_3'] = 0
		context['paginador_atras_2'] = 0
		context['paginador_atras_1'] = 0
		context['paginador_alante_5'] = 0
		context['paginador_alante_4'] = 0
		context['paginador_alante_3'] = 0
		context['paginador_alante_2'] = 0
		context['paginador_alante_1'] = 0
		return

	paginator = Paginator(model_rows, pags_per_page)

	pag_sel = int(pag_sel)
	if pag_sel < 1:
		pag_sel = 1
	if pag_sel > paginator.num_pages:
		pag_sel = paginator.num_pages

	try:
		data = paginator.page(pag_sel)
	except:
		data = paginator.page(1)

	es_paginado = True if paginator.num_pages > 1 else False

	if not data:
		data = []
	context['data'] = data
	context['total_resultados'] = len(model_rows)
	context['es_paginado'] = es_paginado
	context['pagina'] = pag_sel
	context['registros_por_pagina'] = pags_per_page
	context['paginador_ultima_pagina'] = (paginator.num_pages)
	context['paginador_atras_5'] = (pag_sel - 5) > 1
	context['paginador_atras_4'] = (pag_sel - 4) > 1
	context['paginador_atras_3'] = (pag_sel - 3) > 1
	context['paginador_atras_2'] = (pag_sel - 2) > 1
	context['paginador_atras_1'] = (pag_sel - 1) > 1
	context['paginador_alante_5'] = (pag_sel + 5) < paginator.num_pages
	context['paginador_alante_4'] = (pag_sel + 4) < paginator.num_pages
	context['paginador_alante_3'] = (pag_sel + 3) < paginator.num_pages
	context['paginador_alante_2'] = (pag_sel + 2) < paginator.num_pages
	context['paginador_alante_1'] = (pag_sel + 1) < paginator.num_pages
	return


def get_server_url(request, query_url):

	server = "%s://%s" % (request.scheme, request.META['HTTP_HOST'])
	if (query_url[0] == "/"):
		query_url = query_url[1:]
	url = "%s/%s" % (server, query_url)
	return url


def is_int(s):
	if s is None:
		return False  # Si s es None, no es un float válido
	try:
		int(s)
		return True
	except:
		return False


def is_float(s):
	if s is None:
		return False  # Si s es None, no es un float válido
	try:
		float(s)
		return True
	except:
		return False

def is_bool(s):
	try:
		if s == 1 or s is True or s == "1":
			return 1
	except:
		return False
	return False

def get_str_value_from_int(value):

	if value is None:
		return "0"
	try:
		value = int(value)
		return str(value)
	except:
		return "0"


def get_value_from_int(value):

	if value is None:
		return 0
	try:
		value = int(value)
		return value
	except:
		return 0


def get_str_value_from_bool(value):

	if value is None:
		return "0"
	if (str(value) == "1"):
		return "1"
	if (str(value).upper() == "TRUE"):
		return "1"
	if (value is True):
		return "1"
	return "0"


def get_value_from_bool(value):

	value = get_str_value_from_bool(value);
	if value == "1":
		return True
	return False


def get_form_post_field(request, form_id, submit_button_name):

	if request.method == 'POST':
		if request.POST:
			if request.POST.get('form_id') == form_id:
				if submit_button_name in request.POST:
					return request.POST.get(submit_button_name)


def get_realuser_is_superuser(request):

	realuser = getattr(request, "user")
	if realuser:
		is_superuser = getattr(realuser, "is_superuser")
		if is_superuser:
			return True
	return False


def get_system_timezone():

	from zoneinfo import ZoneInfo
	from project.settings import TIME_ZONE
	return ZoneInfo(TIME_ZONE)


def get_user_admin():
	from django.contrib.auth import get_user_model
	User = get_user_model()
	try:
		user_apikey = User.objects.get(username="admin")
		return user_apikey
	except User.DoesNotExist:
		return None

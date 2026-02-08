# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

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


def load_view(request, form_name, with_context = {}):

	template = loader.get_template(form_name)
	return HttpResponse(template.render(with_context, request))


def form_login(request):
	return load_view(request, 'admin/login.html')


def action_login(request):

	# Creamos el formulario de autenticación vacío
	form = AuthenticationForm()
	if request.method == "POST":

		# if not validate_captcha(request):
		# 	return form_login(request)

		# Añadimos los datos recibidos al formulario
		form = AuthenticationForm(request=request, data=request.POST)
		# Si el formulario es válido
		if form.is_valid():
			# Recuperamos las credenciales validadas
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user_found = User.objects.filter(username=username).first()
			if not user_found:  # El usuario no existe
				messages.add_message(request, messages.ERROR, _('Nombre de usuario o contraseña incorrecto'))
				return form_login(request)

			# Verificamos las credenciales del usuario
			user = authenticate(request=request, username=username, password=password)

			# Si existe un usuario con ese nombre y contraseña
			if user is not None:
				# Hacemos el login manualmente
				do_login(request, user)
				# Y le redireccionamos al home con un mensajito
				return redirect('/')

	messages.add_message(request, messages.ERROR, _('Nombre de usuario o contraseña incorrecto'))
	return form_login(request)


def action_logout(request):

	messages.add_message(request, messages.INFO, _('Hasta la proxima %s. Gracias por tu visita') % request.user.username)
	do_logout(request)
	return redirect('/')

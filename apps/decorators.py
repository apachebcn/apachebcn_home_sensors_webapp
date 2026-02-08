# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from functools import wraps

from django.core.exceptions import PermissionDenied
from apps.common_functions import get_realuser_is_superuser

import logging
logger = logging.getLogger('django')

APIKEY_PASS = "XCDEFGHI1234221390"


def superuser_required(view_func):
	"""
	Decorador que permite el acceso solo a superusuarios.
	Si el usuario no es un superusuario, devuelve un error 403.
	"""

	from django.core.exceptions import PermissionDenied

	def _wrapped_view(request, *args, **kwargs):
		if not get_realuser_is_superuser(request):
			raise PermissionDenied("Permission denied.")
		return view_func(request, *args, **kwargs)
	return _wrapped_view


def apikey_required(app_name):
	"""
	Decorador que permite el acceso solo a superusuarios.
	Si el usuario no es un superusuario, devuelve un error 403.
	"""
	def decorador(view_func):
		@wraps(view_func)  # Mantiene los metadatos de la vista original
		def _wrapped_view(request, *args, **kwargs):

			apikey = request.GET.get("apikey", None)
			if not apikey:
				raise PermissionDenied("fault apikey")

			if apikey != APIKEY_PASS:
				raise PermissionDenied("wrong apikey")

			# Llamar a la vista original si todo está bien
			return view_func(request, *args, **kwargs)

		return _wrapped_view
	return decorador

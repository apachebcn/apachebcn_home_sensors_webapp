# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

# context_processors.py

from project import settings
from django.contrib.auth.models import User
from django import get_version

import logging
logger = logging.getLogger('django')


def context_procesor_user_env(request):

	user = getattr(request, "user", None)
	if not user:
		user = get_current_user()

	is_superuser = False
	if user:
		is_superuser = getattr(user, "is_superuser", False)

	context = {
		'django_version': get_version(),
		'debug_mode': settings.DEBUG,
		'list_users': {},
	}

	if user and is_superuser:
		users = User.objects.exclude(id=user.id).all()
		list_users = []
		for user in users:
			list_users.append({
				'id': user.pk,
				'nombre': user.username  # Puedes ajustar qué información quieres mostrar de cada usuario
			})
		if (list_users):
			context['list_users'] = list_users

	return context

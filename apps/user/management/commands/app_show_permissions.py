# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import logging
logger = logging.getLogger('django')


class Command(BaseCommand):

	help = 'Mostrar permisos en el sistema'

	def handle(self, *args, **kwargs):

		for permission in Permission.objects.all():
			print(permission.codename)

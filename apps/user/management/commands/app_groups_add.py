# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

import logging
logger = logging.getLogger('django')


class Command(BaseCommand):

	help = 'Añadir grupos y permisos para los usuarios'

	def process_permissions_group(self, content_type, permissions, group_name):

		user_manager_group, created = Group.objects.get_or_create(name=group_name)

		for codename in permissions:
			# Intentar obtener el permiso existente
			try:
				permission = Permission.objects.get(
					codename=codename,
					content_type=content_type,
				)
			except Permission.DoesNotExist:
				logger.error(f"No existe el permiso '{codename}'")
				exit(1)

			if not permission:
				logger.error(f"No existe el permiso '{codename}'")
				exit(1)

			# Asignar el permiso al grupo UserManager si no lo tiene
			if permission not in user_manager_group.permissions.all():
				user_manager_group.permissions.add(permission)


	def handle(self, *args, **kwargs):

		# Crear group UsertTranslator
		user_manager_group, created = Group.objects.get_or_create(name='UserTranslator')

		# Crear group UserHistoryDataExport
		_, _ = Group.objects.get_or_create(name='UserHistoryDataExport')

		# Crear group UserHistoryDataImport
		_, _ = Group.objects.get_or_create(name='UserHistoryDataImport')


		"""
			PERMISOS DE UserManager/InputData
		"""
		# Obtener el content type para InputData
		from apps.input_data.models import InputData
		content_type = ContentType.objects.get_for_model(InputData)
		# Definir permisos: add, change y delete para InputData
		permissions = [
			'view_inputdata',
		]
		self.process_permissions_group(content_type, permissions, "UserManager")


		"""
			PERMISOS DE UserManager/InputDataHistory
		"""
		# Obtener el content type para InputDataHistory
		from apps.input_data_history.models import InputDataHistory
		content_type = ContentType.objects.get_for_model(InputDataHistory)
		# Definir permisos: add, change y delete para InputDataHistory
		permissions = [
			'delete_inputdatahistory',
			'view_inputdatahistory',
		]
		self.process_permissions_group(content_type, permissions, "UserManager")


		self.stdout.write(self.style.SUCCESS('UserManager group setup complete'))

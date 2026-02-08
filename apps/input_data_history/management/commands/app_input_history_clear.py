# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.input_data_history.models import InputDataHistory

import logging
logger = logging.getLogger('django')


class Command(BaseCommand):

	# TODO: ESTO TE MUESTRA EN LA AYUDA DEL COMANDO
	help = 'Borra todos los datos historicos de un usuario'


	def add_arguments(self, parser):

		# TODO: ESTO TE RECOGE EL ARGUMENTO user_id Y TE EXPLICA QUE ES EN EL HELP
		parser.add_argument('user_id', type=int, help='ID del usuario para eliminar sus registros')


	def handle(self, *args, **kwargs):

		# TODO: COGE EL user_id DEL COMANDO DE LA CONSOLA
		user_id = kwargs['user_id']

		try:
			# TODO: COJE LA FILA USER DE LA BASE DE DATOS, CUYO user_id ES LO QUE HAS PUESTO EN EL COMANDO
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			# TODO: EL user_id QUE HAS PUESTO NO EXISTE Y TE DOY EL ERROR
			self.stdout.write(self.style.ERROR(f'Usuario con ID {user_id} no encontrado'))
			return

		# TODO: BORRO DE LA BASE DE DATOS "InputDataHistory" TODOS LOS DATOS DEL user_id QUE LE HE INDICADO EN EL COMANDO
		deleted_count, _ = InputDataHistory.objects.filter(user_id=user).delete()

		# TODO: MENSAJE BONITO EN VERDE EN LA CONSOLA
		self.stdout.write(self.style.SUCCESS(f'Se eliminaron {deleted_count} registros para el usuario con ID {user_id}'))

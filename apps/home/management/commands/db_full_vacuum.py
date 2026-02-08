# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.core.management.base import BaseCommand
from django.db import connection

"""
	Arregla todos los nextids de la base de datos
"""

class Command(BaseCommand):
	help = 'Arregla todos los nextids de la base de datos'


	def handle(self, *args, **kwargs):

		with connection.cursor() as cursor:
			self.stdout.write("Ejecutando VACUUM FULL en toda la base de datos...")
			cursor.execute("VACUUM FULL;")
			self.stdout.write(self.style.SUCCESS("VACUUM FULL completado correctamente"))

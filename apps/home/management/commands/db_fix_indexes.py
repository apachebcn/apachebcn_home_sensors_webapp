# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.core.management.base import BaseCommand
import os
import psycopg2

"""
	Arregla todos los nextids de la base de datos
"""

class Command(BaseCommand):
	help = 'Arregla todos los nextids de la base de datos'


	def handle(self, *args, **kwargs):

		PG_DB = os.getenv("DB_NAME")
		PG_USER = os.getenv("DB_USER")
		PG_PASS = os.getenv("DB_PASSWORD")

		conn = psycopg2.connect(
			host="db",
			database=PG_DB,
			user=PG_USER,
			password=PG_PASS
		)

		self.fix_all_sequences(conn)
		conn.close()

		self.stdout.write(self.style.SUCCESS('FIN'))


	def fix_all_sequences(self, connection):
		"""
		Recorre todas las tablas que tengan columnas con secuencia y ajusta la secuencia
		al valor máximo actual de la columna 'id' para evitar conflictos.
		"""
		with connection.cursor() as cursor:
			# Obtener todas las secuencias relacionadas con columnas serial (id)
			cursor.execute("""
				SELECT
					sequence.relname as sequence_name,
					tab.relname as table_name,
					attr.attname as column_name
				FROM
					pg_class sequence
					JOIN pg_depend dep ON dep.objid = sequence.oid
					JOIN pg_class tab ON dep.refobjid = tab.oid
					JOIN pg_attribute attr ON attr.attrelid = tab.oid AND attr.attnum = dep.refobjsubid
				WHERE
					sequence.relkind = 'S';
			""")
			sequences = cursor.fetchall()

			for sequence_name, table_name, column_name in sequences:
				# Obtener el valor máximo actual del campo id (o el campo con secuencia)
				cursor.execute(f"SELECT MAX({column_name}) FROM {table_name}")
				max_id = cursor.fetchone()[0] or 0

				# Ajustar la secuencia al max_id o 1 si no hay registros
				next_val = max_id if max_id > 0 else 1

				cursor.execute(f"SELECT setval('{sequence_name}', {next_val}, true)")
				print(f"Sequence {sequence_name} for {table_name}.{column_name} fixed to {next_val}")

		connection.commit()

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
	try:
		from django.core.management import execute_from_command_line
	except ImportError as exc:
		raise ImportError(
			"Couldn't import Django. Are you sure it's installed and "
			"available on your PYTHONPATH environment variable? Did you "
			"forget to activate a virtual environment?"
		) from exc

	# Revisar el comando ejecutado
	command = sys.argv[1] if len(sys.argv) > 1 else None
	mode = os.getenv('MODE', 'DEV')

	# Detectar entorno VSCode
	in_vscode = (
		os.getenv('VSCODE_PID') or
		os.getenv('DJANGO_VSCODE') or
		'--noreload' in sys.argv or
		'--nothreading' in sys.argv or
		(command and 'runserver' in command)
	)

	# Activar debug solo en entorno VSCode y comando relacionado con servidor
	if mode == 'DEV' and in_vscode:
		if os.path.exists("./project/debug_py.py") and os.environ.get("DJANGO_DEBUG_PY", False):
			print("| *************************************")
			print("| *                                   *")
			print("| *        EJECUTANDO DEBUGPY         *")
			print("| *                                   *")
			print("| *************************************")
			from project import debug_py
		elif os.path.exists("./project/debug_ptvsd.py") and os.environ.get("DJANGO_DEBUG_PTVSD", False):
			print("| *************************************")
			print("| *                                   *")
			print("| *        EJECUTANDO PYTVSD          *")
			print("| *                                   *")
			print("| *************************************")
			from project import debug_ptvsd


	execute_from_command_line(sys.argv)

if __name__ == '__main__':
	main()

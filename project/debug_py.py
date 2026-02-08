# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

import os
import debugpy
import subprocess

def is_debugpy_running():
	try:
		# Buscar el proceso de debugpy con 'ps' en el contenedor
		output = subprocess.check_output(["ps", "aux"], text=True)
		return any("debugpy" in line for line in output.splitlines())
	except Exception as e:
		print(f"Error checking debugpy process: {e}")
		return False

if is_debugpy_running():
	print("Debugpy ya está escuchando en el puerto 3000")

if not is_debugpy_running():
	try:
		debugpy.listen(("0.0.0.0", 3000))  # Cambia el puerto si es necesario
	except:
		pass
	# debugpy.wait_for_client()  # Opcional: Pausa la ejecución hasta que un cliente se conecte

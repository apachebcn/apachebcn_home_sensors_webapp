#!/bin/bash

echo "*************************************"
echo "*    Starting Jupyter Notebook      *"
echo "*************************************"

# Este script se debe ejecutar en la misma instancia que el contendor
# osea:
#   docker exec -u django -ti django_webs_django /srv/project/run_jupyter.sh


# En kernelspec list debe verse el kernel 'django-shell-plus' que es el que debe usarse en 
jupyter kernelspec list


echo "port: ${EXPOSE_PUBLIC_PORT_DJANGO_JUPYTER}"

jupyter notebook --ip=0.0.0.0 --port=${EXPOSE_PUBLIC_PORT_DJANGO_JUPYTER} --no-browser --NotebookApp.allow_remote_access=True --NotebookApp.token='' --allow-root --notebook-dir=/srv/project/jupyter_notebooks



: << 'END'

# Ejemplo de codigo en jupyter
import os
import sys
import django

# Agrega la ruta del proyecto al PYTHONPATH
sys.path.append('/srv/project')

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# Importa el modelo
from apps.cms_page.models import CmsPage

# Ejecuta la consulta de forma directa
page = CmsPage.objects.get(id=1)
print(page.id)

END
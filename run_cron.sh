#!/bin/bash

# NO BORRAR, LO EJECUTA DOCKER PARA INICIAR CRON
while true; do
    python /srv/project/manage.py runcrons
    sleep 60
done

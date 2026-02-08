# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.conf import settings

import smtplib

EMAIL_HOST = settings.DJANGO_EMAIL_HOST
EMAIL_PORT = settings.DJANGO_EMAIL_PORT
EMAIL_HOST_USER = settings.DJANGO_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.DJANGO_EMAIL_HOST_PASSWORD

try:
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        print("Conexión exitosa con el servidor SMTP.")
except Exception as e:
    print(f"Error en la conexión SMTP: {e}")

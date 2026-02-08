# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

import os
import django
from django.conf import settings
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')  # Ajusta esto según tu estructura
django.setup()

# Configuración del correo electrónico
settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
email_to = settings.EMAIL_HOST_USER

print(f"EMAIL_BACKEND = {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST = {settings.EMAIL_HOST}")
print(f"EMAIL_USE_TLS = {settings.EMAIL_USE_TLS}")
print(f"EMAIL_USE_SSL = {settings.EMAIL_USE_SSL}")
print(f"EMAIL_PORT = {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER = {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD = {settings.EMAIL_HOST_PASSWORD}")
print(f"DEFAULT_FROM_EMAIL = {settings.DEFAULT_FROM_EMAIL}")

# Enviar un correo de prueba
try:
    # Mensaje simple sin caracteres especiales
    subject = 'Test Email'  # Asunto
    message = 'This is a test email.'  # Mensaje

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Desde
        [email_to],  # Para
        fail_silently=False,
    )
    print(f"Correo enviado exitosamente a {email_to}")
except Exception as e:
    print(f"Error al enviar el correo: {str(e)}")

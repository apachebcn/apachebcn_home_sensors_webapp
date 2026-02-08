"""
	minicaptcha 2020
	by Pedro Reina (apachebcn@gmail.com)
"""

from django.db import models


class CaptchaRespuestas(models.Model):

	respuesta_uuid = models.CharField(max_length = 100, blank = False, null = False, unique = True)
	respuesta_text = models.CharField(max_length = 50, blank = False, null = False, unique = False)
	creado = models.DateTimeField(auto_now_add=True)

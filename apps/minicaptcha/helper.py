"""
	minicaptcha 2020
	by Pedro Reina (apachebcn@gmail.com)
"""

import uuid
from apps.minicaptcha.models import CaptchaRespuestas
from project import settings
from django.utils.translation import gettext as _
from django.contrib import messages

from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
from PIL import Image
import random
import os

"""
	Genera una cadena alfanumerica, la convierte en imagen y lo almacen en MEDIA_ROOT+"/captchas/"
	Retorna la cadena y la url de la imagen
"""


def generate_random_word(word_long):

	number = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	captcha_text = []
	for i in range(word_long):
		c = random.choice(number)
		captcha_text.append(c)
	captcha_text = ''.join(captcha_text)
	return captcha_text


def generate_captcha():

	# Limpieza de ficheros, elimino los captcha que no son del día actual
	path = settings.MEDIA_ROOT + "/captchas"
	from django.utils import timezone
	import time
	now = timezone.now()
	from os import scandir
	ficheros = scandir(path)
	for fichero in ficheros:
		if fichero.is_file():
			fichero_fecha = os.path.getmtime(fichero)
			file_day = int(time.strftime('%d', time.localtime(fichero_fecha)))
			if file_day != now.day:
				from os import remove
				remove(fichero)

	captcha_text = generate_random_word(6)
	WIDTH = 250
	HEIGHT = 100
	image = ImageCaptcha(width = WIDTH, height = HEIGHT, font_sizes = [80])

	import hashlib
	result = hashlib.md5(captcha_text.encode())
	captcha_text_encripted = result.hexdigest()
	if not os.path.isdir(path):
		os.mkdir(path)

	filename = path + "/%s.png" % captcha_text_encripted
	url = "/media/captchas/%s.png" % captcha_text_encripted
	if not os.path.isfile(filename):
		captcha = image.generate(captcha_text)
		captcha_image = Image.open(captcha)
		captcha_image = np.array(captcha_image)
		image.write(captcha_text, filename)
	return captcha_text, url


def set_captcha(request):

	# Genero el captcha
	respuesta_text, url = generate_captcha()

	# Borrar todos los registros excepto los 100 ultimos
	objects_to_keep = CaptchaRespuestas.objects.filter().order_by('-creado')[:100]
	CaptchaRespuestas.objects.exclude(pk__in=objects_to_keep).delete()

	respuesta_uuid = str(uuid.uuid4())
	captcha_model = CaptchaRespuestas(respuesta_uuid = respuesta_uuid, respuesta_text = respuesta_text)
	captcha_model.save()
	request.session['captcha'] = respuesta_uuid

	return """
<div class='mini-captcha-div-main' style='border:1px solid lightgray; border-radius:5px;padding:15px;'>
	<div class='mini-captcha-div-image' style='width:300px;float:left'>
		<img src="%s?%s"/>
	</div>
	<div class="form-row" style="display:inline-flex">
		<label class="required" for="id_username">%s:&nbsp;&nbsp;</label>
		<input type="text" name="captcha_answer" autofocus="" autocapitalize="none" autocomplete="off" maxlength="10" required="required" id="id_captcha_answer">
	</div>
</div>""" % (url, generate_random_word(30).lower(), _('Escribe el captcha'))


def validate_captcha(request):

	if not request.POST:
		messages.add_message(request, messages.ERROR, 'Captcha no POST data')
		return False

	validate_user = request.POST.get('captcha_answer')
	if not validate_user or validate_user is None:
		return False

	if 'captcha' not in request.session:
		return False

	respuesta_uuid = request.session['captcha']
	# print("respuesta = %s" % respuesta_uuid)
	row = CaptchaRespuestas.objects.filter(respuesta_uuid = respuesta_uuid).first()
	respuesta_text = row.respuesta_text
	# print("respuesta_text = %s" % respuesta_text)

	if (validate_user.upper() == respuesta_text.upper()):
		return True

	messages.add_message(request, messages.ERROR, _('Captcha incorrecto'))
	return False

# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.input_data.models import InputData

import logging
logger = logging.getLogger('django')


"""
	PÁGINA HOME
"""
@login_required(login_url='/form_login/')
def home_view(request):

	if request.POST:
		if request.POST.get('action') == "reset-stat":
			if 'fieldname' in request.POST:
				input_data = InputData.objects.filter(user_id=request.user).first()
				if input_data:
					fieldname = request.POST.get('fieldname')
					if fieldname:
						setattr(input_data, fieldname + "_min", None)
						setattr(input_data, fieldname + "_max", None)
						input_data.save()
				input_data = InputData.objects.filter(user_id=request.user).first()
	context = {
		'title': format_html(_("Datos")),
		'room_id': "Número de dispositivo",
		'data_temp_title':"Temperatura",
		'data_hum_title':"Humedad",
	}
	return render(request, 'pages/home.html', context)


def admin_tools(request):

	return render(request, 'pages/admin_tools.html', {'title': 'ADMIN TOOLS'})

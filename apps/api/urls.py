"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [

	# Inserta los datos recibidos en la base de datos
	path('api/write_data/', views.write_input_data_view, name='write_input_data_view'),

	# Es llamado por javascript desde la vista graph_history.html
	path('api/get_json_sensors_graph_temp_view/', views.api_get_json_sensors_graph_temp_view, name='api_get_json_sensors_graph_temp_view'),
	path('api/get_json_sensors_graph_hum_view/', views.api_get_json_sensors_graph_hum_view, name='api_get_json_sensors_graph_hum_view'),

]

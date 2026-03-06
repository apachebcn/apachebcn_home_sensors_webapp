# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial


from apps.api.helper import api_get_json_sensors_temp_graph
from apps.api.helper import api_get_json_sensors_hum_graph
from .helper import insert_input_data

import logging
logger = logging.getLogger('django')



def api_get_json_sensors_graph_temp_view(request):
	# Es llamado por javascript desde la vista graph_history.html
	return api_get_json_sensors_temp_graph(request)

def api_get_json_sensors_graph_hum_view(request):
	# Es llamado por javascript desde la vista graph_history.html
	return api_get_json_sensors_hum_graph(request)


def write_input_data_view(request):
	return insert_input_data(request)

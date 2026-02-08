# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial


from apps.api.helper import api_realtime_data_graph, api_get_json_data_graph
from .helper import insert_input_data

import logging
logger = logging.getLogger('django')


def api_realtime_data_graph_view(request):
	# Es llamado por javascript desde la vista graph_realtime.html
	return api_realtime_data_graph(request)


def api_get_json_data_graph_view(request):
	# Es llamado por javascript desde la vista graph_history.html
	return api_get_json_data_graph(request)


def write_input_data_view(request):
	return insert_input_data(request)


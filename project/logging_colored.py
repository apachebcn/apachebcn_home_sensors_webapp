# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial


from colorama import init, Fore, Back, Style
import logging


TRAPHIC_LEVEL = 25
logging.addLevelName(TRAPHIC_LEVEL, 'TRAPHIC')

CACHE_LEVEL = 26
logging.addLevelName(CACHE_LEVEL, 'CACHE')

def traphic(self, message, *args, **kws):
	if self.isEnabledFor(TRAPHIC_LEVEL):
		self._log(TRAPHIC_LEVEL, message, args, **kws)

def cache(self, message, *args, **kws):
	if self.isEnabledFor(TRAPHIC_LEVEL):
		self._log(CACHE_LEVEL, message, args, **kws)


logging.Logger.traphic = traphic
logging.Logger.cache = cache

class ColoredFormatter(logging.Formatter):
	"""Formatter que aplica colores a los niveles de logging."""

	def format(self, record):
		# Definir colores para cada nivel de log
		log_colors = {
			logging.DEBUG: Fore.YELLOW,
			logging.INFO: Fore.CYAN,
			logging.WARNING: Fore.GREEN,
			logging.ERROR: Fore.RED,
			logging.CRITICAL: Fore.RED + Style.BRIGHT,
			CACHE_LEVEL: Fore.BLACK + Back.YELLOW,
			TRAPHIC_LEVEL: Fore.BLACK + Back.GREEN,
		}

		# Obtener el color para el nivel del log actual
		color = log_colors.get(record.levelno, Fore.WHITE)

		# Definir el formato del log
		log_fmt = f'{color}%(levelname)s %(name)s %(message)s - [%(pathname)s %(funcName)s:%(lineno)d] %(asctime)s{Style.RESET_ALL}'

		date_fmt = '%d-%m-%Y %H:%M:%S'  # Formato de fecha simplificado

		formatter = logging.Formatter(fmt=log_fmt, datefmt=date_fmt)
		return formatter.format(record)

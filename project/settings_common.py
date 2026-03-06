"""
	Este fichero es parte de la construcción automatica del settings.py
	Se combina éste (config_settings_common.py) con config_settings_dev.py o config_settings_mode.py según sea el modo seleccionado desde el comando 'invoke' desde la raíz del docker de éste proyecto.

	Los bloques cuyos comentarios mencionan "# DJANGO ENV - " son variables que deben estar definidos en el entorno de docker.

	Para generar o regenerar el settings.py, hay que hacer desde la raiz del docker:
	$ invoke dev
	ó
	$ invoke prod

	Y para ejecutar los contenedores del proyecto:
	$ invoke up
"""

# start content for invoke
import os
from django.utils.translation import gettext_lazy as _

print_os_vars = False

def _get_env_bool_value(name):
	if name not in os.environ:
		raise Exception(f"{name} not in environment")
	value = os.getenv(name)
	if value is None: return False
	if value is False: return False
	if value is True: return True
	if value.lower() == 'true': return True
	if value.lower() == 'false': return False
	return False

def _get_env_int_value(name, default = ""):
	if name not in os.environ:
		raise Exception(f"{name} not in environment")
	value = os.getenv(name, default)
	try:
		return int(value)
	except (ValueError, TypeError):
		return default

def get_env_value(name, type_var = 'char', default = ""):
	if name not in os.environ:
		raise Exception(f"{name} not in environment")
	if type_var == 'char':
		value = os.getenv(name, default)
		if print_os_vars:
			print(f"{name} = {value}")
		return value
	if type_var == 'int':
		value = _get_env_int_value(name, default)
		if print_os_vars:
			print(f"{name} = {value}")
		return value
	if type_var == 'bool':
		value = _get_env_bool_value(name)
		if print_os_vars:
			print(f"{name} = {value}")
		return value
	return value

# Configuración básica
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# descomentar si necesitas ver toda la lista de variables de entorno pasado por docker
# print("OS VARS")
# env_vars = {key: value for key, value in os.environ.items() if key.startswith("DJANGO_") or key.startswith("DATABASE_")}
# print(env_vars)

# URL para acceder al panel de administración
# Reemplaza 'admin' con un nombre personalizado por razones de seguridad
# No debe llevar barras, ni al principio, ni al final
SECRET_ADMIN_URL_WORD = get_env_value('DJANGO_SECRET_ADMIN_URL_WORD', 'char')

# DJANGO ENV - Django settings (provienen de docker environment)
MODE = get_env_value('MODE')
FORCE_HTTP = get_env_value('DJANGO_FORCE_HTTP', 'bool')
HTTPS_MODE = get_env_value('DJANGO_HTTPS_MODE')
DISABLED_CSRF = get_env_value('DJANGO_DISABLED_CSRF', 'bool')
DEBUG = get_env_value('DJANGO_DEBUG', 'bool', False)
DEBUG_TOOLBAR = get_env_value('DJANGO_DEBUG_TOOLBAR', 'bool')
DEBUG_PTVSD = get_env_value('DJANGO_DEBUG_PTVSD', 'bool')
DEBUG_PY = get_env_value('DJANGO_DEBUG_PY', 'bool')
LOG_LEVEL = get_env_value('DJANGO_LOG_LEVEL')
LOG_LEVEL = LOG_LEVEL.upper()
DJANGO_SEND_MAIL_ON_ERROR_ENABLE = get_env_value("DJANGO_SEND_MAIL_ON_ERROR_ENABLE", 'bool')
DJANGO_SEND_MAIL_ON_ERROR_SITE_NAME_FOR_SUBJECT = get_env_value("DJANGO_SEND_MAIL_ON_ERROR_SITE_NAME_FOR_SUBJECT")

# DJANGO ENV - Django Security settings (provienen de docker environment)
SECRET_KEY = get_env_value('DJANGO_SECRET_KEY')
SECURE_SSL_REDIRECT = get_env_value('DJANGO_SECURE_SSL_REDIRECT', 'bool')
DJANGO_SECURE_PROXY_SSL_HEADER = get_env_value('DJANGO_SECURE_PROXY_SSL_HEADER', 'bool')
if DJANGO_SECURE_PROXY_SSL_HEADER:
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ROUTE_ONLY_IP = get_env_value('DJANGO_ROUTE_ONLY_IP')  # Esta variable no es natural de django (Para limitar el acceso a una IP concreta

# DJANGO ENV - Django Security sesion cookie (provienen de docker environment)
SESSION_COOKIE_HTTPONLY = get_env_value('DJANGO_SESSION_COOKIE_HTTPONLY', 'bool')
CSRF_COOKIE_SECURE = get_env_value('DJANGO_CSRF_COOKIE_SECURE', 'bool')
SESSION_COOKIE_SECURE = get_env_value('DJANGO_SESSION_COOKIE_SECURE', 'bool')
CSRF_COOKIE_SAMESITE = get_env_value('DJANGO_CSRF_COOKIE_SAMESITE')
SESSION_COOKIE_NAME = get_env_value('DJANGO_SESSION_COOKIE_NAME')
SESSION_COOKIE_AGE = get_env_value('DJANGO_SESSION_COOKIE_AGE', 'int')
SESSION_EXPIRE_AT_BROWSER_CLOSE = get_env_value('DJANGO_SESSION_EXPIRE_AT_BROWSER_CLOSE')

# DJANGO ENV - Django email parameters (provienen de docker environment)
EMAIL_HOST = get_env_value('DJANGO_EMAIL_HOST')
EMAIL_USE_TLS = get_env_value('DJANGO_EMAIL_USE_TLS', 'bool')
EMAIL_USE_SSL = get_env_value('DJANGO_EMAIL_USE_SSL', 'bool')
EMAIL_PORT = get_env_value('DJANGO_EMAIL_PORT')
EMAIL_HOST_USER = get_env_value('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_value('DJANGO_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = get_env_value('DJANGO_EMAIL_DEFAULT_FROM')
SERVER_EMAIL = get_env_value('DJANGO_EMAIL_DEFAULT_FROM')

# DJANGO ENV - jango DB parameters (provienen de docker environment)
DB_POSTGRES_VERSION = get_env_value('DB_POSTGRES_VERSION')
DB_ENGINE = get_env_value('DB_ENGINE')
DB_HOST = get_env_value('DB_HOST')
DB_NAME = get_env_value('DB_NAME')
DB_USER = get_env_value('DB_USER')
DB_PASSWORD = get_env_value('DB_PASSWORD')
DB_PORT = get_env_value('DB_PORT')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Configuración del modo de ejecución
if not MODE or MODE not in ["DEV", "PROD"]:
	raise Exception(f"ERROR: La variable de entorno MODE no está definida correctamente. Valor = '{MODE}'")

# Almacenamiento de cookies
DJANGO_SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Configuración de Axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCK_OUT_AT_FAILURE = True
AXES_BEHIND_REVERSE_PROXY = True

# Aplicaciones
MY_APPS = [
	'apps.minicaptcha',
	'apps.user',
	'apps.home',
	'apps.input_data',
	'apps.input_data_history',
	'apps.custom_user_admin',
]

INSTALLED_APPS = [
	'django_extensions',
	'django_ptvsd',
	'adminlte3',  # General use templates & template tags (should appear first)
	#'adminlte3_theme',  # Optional: Django admin theme (must be before django.contrib.admin) NO FUNCIONA BIEN, BUG EN EL ORDERBY
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.humanize',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rangefilter',
	'bootstrap4',
	'django_sb_admin',
 	'axes',
	# 'jquery',  # De momento no lo necesito y es mejor no usarlo
] + MY_APPS


if MODE == "DEV":
	INSTALLED_APPS += ['werkzeug_debugger_runserver']


ADMIN_REORDER = [
	{
		'app': 'auth',
		'models': ('auth.User', 'auth.Group', ),
	},
	{
		'app': 'input_data',
		'label': _('Datos'),
		'models': ('input_data.InputData', 'input_data_history.InputDataHistory', ),
	},

]


# Middleware
MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'admin_reorder.middleware.ModelAdminReorder',
	'axes.middleware.AxesMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

# Autenticación
AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',  # Este es el backend por defecto
	'django_su.backends.SuBackend',  # Añadir este backend para soportar django-su
	'axes.backends.AxesStandaloneBackend',  # Usa AxesStandaloneBackend para la protección de inicio de sesión
)

# Templates
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR + '/templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'apps.context_processors.context_procesor_user_env',
				'django_su.context_processors.is_su',
			],
			'builtins': [
				'django.templatetags.static',
				'django.templatetags.i18n',
			],
		},
	},
]

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
	# {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
	# {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # Comento este para poder indicar contraseñas cortas
	# {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # Comento este para poder indicar contraseñas comunes
	# {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # Comento este para poder indicar contraseñas numéricas
]

# Configuración de zona horaria e internacionalización
TIME_ZONE = 'Europe/Madrid'
USE_TZ = True  # asegúrate de que esté activado

LANGUAGE_CODE = 'es'
ugettext = lambda s: s
LANGUAGES = (
	('es', ugettext('Español')),
)
LOCALE_PATHS = (
	BASE_DIR + '/locale',
)
USE_I18N = True
USE_L10N = True
I18N_URLS = True
PREFIX_DEFAULT_LANGUAGE = True

# Rutas
ROOT_URLCONF = 'project.urls'
#WSGI_APPLICATION = 'project.wsgi.application'
STATICFILES_DIRS = ('/srv/project/assets/static',)
STATIC_ROOT = '/srv/static'
STATIC_URL = "/static/"
MEDIA_ROOT = '/srv/project/assets/media'
MEDIA_URL = "/media/"

# Configuración de logging
# from logging.handlers import RotatingFileHandler
from .logging_colored import ColoredFormatter
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'colored': {
			'()': ColoredFormatter,
		},
		'default': {
			'format': '{asctime} {levelname} {name} {message}',
			'style': '{',
		},
		'format_file': {
			'format': '{asctime} {levelname} {name} {message}\n',
			'style': '{',
		},
	},
	'filters': {
		'ignore_404': {
			'()': 'django.utils.log.CallbackFilter',
			'callback': lambda record: record.status_code != 404,
		},
	},
	'handlers': {
		'console': {
			'level': LOG_LEVEL,
			'class': 'logging.StreamHandler',
			'formatter': 'colored',
		},
		'null': {
			'class': 'logging.NullHandler',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'propagate': False,
		},
		'django_Q': {  # Logger para django-q
			'handlers': ['console'],  # Usar el mismo handler de consola
			'level': 'INFO',          # Nivel de log (ajústalo según lo necesites)
			'propagate': False,       # No propagar a loggers superiores
		},
		'django.request': {
			'handlers': ['console'],
			'propagate': False,
			'level': 'CRITICAL',
			'filters': ['ignore_404'],  # Excluir los errores 404
			'propagate': False,
		},
		'werkzeug': {
			'handlers': ['console'],
			'level': LOG_LEVEL,
			'propagate': False,
		},
		'django.security.DisallowedHost': {  # silenciar el error not in ALLOWED_HOSTS
			'handlers': ['null'],
			'level': 'DEBUG',
			'propagate': False,
		},
	},
}


# Configuración de minificación HTML
HTML_MINIFY = True
REMOVE_EMPTY_TAGS = True
REMOVE_COMMENTS = False

# Configuración de sesiones
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = 'mycms_django_sessionid'
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Configuración de base de datos
DATABASES = {
	'default': {
		'ENGINE': os.environ.get('DB_ENGINE'),
		'NAME': os.environ.get('DB_NAME'),
		'USER': os.environ.get('DB_USER'),
		'PASSWORD': os.environ.get('DB_PASSWORD'),
		'HOST': os.environ.get('DB_HOST'),
		'PORT': os.environ.get('DB_PORT'),
	}
}

# Configuración de caché
cache_enable = False

# Configuraciones adicionales de seguridad
# X_FRAME_OPTIONS: Controla cómo el sitio puede ser embebido en iframes
# 'DENY' - No permite que el sitio sea embebido en ningún iframe (más seguro)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de Debug Toolbar
if DEBUG_TOOLBAR:
	INSTALLED_APPS += ['debug_toolbar']
	MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
	import socket
	hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
	INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1"]
	DEBUG_TOOLBAR_CONFIG = {
		'SHOW_TOOLBAR_CALLBACK': lambda request: True if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest' else False,
	}


# Para detectar las ips reales desde dentro de docker
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
TRUSTED_PROXIES = ['127.0.0.1', '::1', '172.0.0.0/8']

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

DEBUG_PROPAGATE_EXCEPTIONS = True

APIKEY_PASS = "XCDEFGHI1234221390"

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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'APP HOME SENSORS'
admin.site.site_title = 'APP HOME SENSORS - Admin Panel'
# admin.site.site_url = 'http://coffeehouse.com/'
admin.site.index_title = 'APP HOME SENSORS - Admin Control'
# admin.empty_value_display = '**Empty**'

url_admin = f"{settings.SECRET_ADMIN_URL_WORD}/"

urlpatterns = [
	path(url_admin, admin.site.urls),                                                     # Para activar el verdadero admin
	# path('django-sb-admin/', include('django_sb_admin.urls')),                            # PARA VER EL SAMPLE DE sb-admin
	path("", include("apps.api.urls")),
	path("", include("apps.home.urls")),
	path("", include("apps.user.urls")),
	path("", include("apps.input_data.urls")),
	path("", include("apps.input_data_history.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from project.settings import DEBUG_TOOLBAR
if DEBUG_TOOLBAR:
	import debug_toolbar
	urlpatterns = [
		path('__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns

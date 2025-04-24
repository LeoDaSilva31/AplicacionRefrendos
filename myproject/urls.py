from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gestiondepermisos/', admin.site.urls),
    path('', include('accounts.urls')),  # Aquí es donde incluyes las rutas de accounts
    path('refrendos/', include('refrendos.urls')),
    path('estadisticas/', include('estadisticas.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
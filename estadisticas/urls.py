from django.urls import path
from . import views

urlpatterns = [
    path('', views.estadisticas_view, name='estadisticas_view'),  # O la vista correspondiente
    # Ruta para ver los detalles de un título o curso específico
    path('detalle/<str:tipo>/<str:nombre>/', views.detalle_refrendo, name='detalle_refrendo'),
]

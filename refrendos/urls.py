from django.urls import path
from . import views

app_name = 'refrendos'  # Espacio de nombres para evitar conflictos

urlpatterns = [
    path('', views.refrendo_list, name='refrendo-list'),
    path('refrendo/add/', views.refrendo_add, name='refrendo-add'),
    path('refrendo/<int:id>/editar/', views.refrendo_edit, name='refrendo-edit'),
    path('refrendo/<int:id>/eliminar/', views.refrendo_delete, name='refrendo-delete'),
    path('refrendo/<int:id>/', views.refrendo_detail, name='refrendo-detail'),
    path('refrendo/buscar/', views.refrendo_search, name='refrendo-search'),
]

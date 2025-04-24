from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserCreateView, UserListView, home, UserDeleteView, user_edit

urlpatterns = [
    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('usuarios/nuevo/', UserCreateView.as_view(), name='user-create'),
    path('usuarios/<int:user_id>/editar/', user_edit, name='user-edit'),
    path('usuarios/<int:pk>/eliminar/', UserDeleteView.as_view(), name='user-delete'),
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

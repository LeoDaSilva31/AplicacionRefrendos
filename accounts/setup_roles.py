# accounts/setup_roles.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def setup_roles():
    # Obtener permisos relacionados al modelo User
    user_ct = ContentType.objects.get_for_model(User)
    
    # Crear o recuperar grupos
    creador, _ = Group.objects.get_or_create(name='creador')
    lector, _ = Group.objects.get_or_create(name='lector')
    editor, _ = Group.objects.get_or_create(name='editor')

    # Permisos
    permisos_crear = Permission.objects.filter(content_type=user_ct, codename__startswith='add_')
    permisos_ver = Permission.objects.filter(content_type=user_ct, codename__startswith='view_')
    permisos_editar = Permission.objects.filter(content_type=user_ct, codename__in=['change_user', 'delete_user'])

    # Asignar permisos a grupos
    creador.permissions.set(permisos_crear)
    lector.permissions.set(permisos_ver)
    editor.permissions.set(permisos_editar | permisos_ver)

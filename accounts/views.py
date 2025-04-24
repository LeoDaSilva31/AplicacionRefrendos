from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

# Autenticación y permisos
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Vistas genéricas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Formularios personalizados
from .forms import CustomUserUpdateForm


# Vista de login con mensaje de error personalizado
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)


# Vista de logout (redirige al login luego de salir)
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


# Vista de inicio protegida (solo usuarios logueados)
@login_required
def home(request):
    return render(request, 'accounts/home.html')


# Vista que muestra el listado de usuarios (requiere permiso para ver)
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    permission_required = 'auth.view_user'


# Vista para crear usuarios (requiere permiso para agregar)
class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user-list')
    permission_required = 'auth.add_user'

    def form_valid(self, form):
        messages.success(self.request, 'El usuario ha sido creado exitosamente.')
        return super().form_valid(form)


# Vista para editar usuarios (requiere permiso para modificar)
class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'is_active']
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user-list')
    permission_required = 'auth.change_user'

    def get_form(self):
        # Se agregan clases de Bootstrap a los campos del formulario
        form = super().get_form()
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        return form


# Vista para eliminar usuarios (requiere permiso para borrar)
class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')
    permission_required = 'auth.delete_user'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'El usuario ha sido eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# Vista manual para editar usuario (requiere permiso para modificar)
@permission_required('auth.change_user', raise_exception=True)
@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'El usuario ha sido actualizado exitosamente.')
            return redirect('user-list')
    else:
        form = CustomUserUpdateForm(instance=user)

    return render(request, 'accounts/user_edit.html', {'form': form})

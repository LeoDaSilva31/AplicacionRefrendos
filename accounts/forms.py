# accounts/forms.py
from django import forms
from django.contrib.auth.models import User

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'is_active': 'Activo',
        }
        help_texts = {
            'username': 'El nombre de usuario debe ser único y contener solo letras, números y algunos símbolos (como @, ., +, -, _).',
            'email': 'Por favor ingresa un correo electrónico válido.',
        }
        error_messages = {
            'username': {
                'required': 'Por favor ingresa un nombre de usuario.',
                'max_length': 'El nombre de usuario no puede tener más de 150 caracteres.',
            },
            'email': {
                'required': 'Por favor ingresa un correo electrónico.',
                'invalid': 'Por favor ingresa una dirección de correo electrónico válida.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

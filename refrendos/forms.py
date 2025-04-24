from django import forms
from .models import Refrendo

class RefrendoForm(forms.ModelForm):
    class Meta:
        model = Refrendo
        fields = [
            'nombre_completo', 'dni', 'numero_refrendo', 'fecha_vencimiento', 
            'fecha_expedicion', 'fecha_salida', 'tipo', 'titulo', 'curso', 
            'archivo_pdf', 'imagen'
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_refrendo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_expedicion': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_salida': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'archivo_pdf': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

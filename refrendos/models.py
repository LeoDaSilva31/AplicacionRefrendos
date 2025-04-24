from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
import numpy as np

class Titulo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

def calcular_dias_habiles(inicio, fin):
    # Cuenta días hábiles entre dos fechas (lunes a viernes)
    return np.busday_count(inicio.isoformat(), fin.isoformat())

def calcular_dias_corridos(inicio, fin):
    return (fin - inicio).days

class Refrendo(models.Model):
    TIPO_CHOICES = [
        ('TITULO', 'De Título'),
        ('CURSO', 'De Curso'),
    ]

    nombre_completo = models.CharField(max_length=255)
    dni = models.CharField(max_length=20)
    numero_refrendo = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    fecha_expedicion = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    titulo = models.ForeignKey('Titulo', on_delete=models.SET_NULL, null=True, blank=True)
    curso = models.ForeignKey('Curso', on_delete=models.SET_NULL, null=True, blank=True)
    archivo_pdf = models.FileField(upload_to='refrendos/pdf/', blank=True, null=True)
    imagen = models.ImageField(upload_to='refrendos/img/', blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    fecha_salida = models.DateField(null=True, blank=True)
    dias_corridos = models.IntegerField(null=True, blank=True)
    dias_habiles = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.fecha_salida and self.fecha_expedicion:
            self.dias_corridos = calcular_dias_corridos(self.fecha_expedicion, self.fecha_salida)
            self.dias_habiles = calcular_dias_habiles(self.fecha_expedicion, self.fecha_salida)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_completo} - {self.numero_refrendo}"

    class Meta:
        permissions = [
            ('ver_refrendo', 'Puede ver refrendos'),
            ('crear_refrendo', 'Puede crear refrendos'),
            ('editar_refrendo', 'Puede editar refrendos'),
            ('borrar_refrendo', 'Puede borrar refrendos'),
        ]

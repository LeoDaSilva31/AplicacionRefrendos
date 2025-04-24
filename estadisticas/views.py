from django.shortcuts import render
from refrendos.models import Refrendo
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q

def estadisticas_view(request):
    # valores que llegan por GET (por defecto “Todos”)
    selected_year  = request.GET.get('year',  'all')
    selected_month = request.GET.get('month', 'all')
    selected_type  = request.GET.get('type',  'TODOS')

    # opciones de años y meses disponibles
    years = (
        Refrendo.objects
        .values_list('fecha_expedicion__year', flat=True)
        .distinct()
        .order_by('fecha_expedicion__year')
    )

    months = [
        {'id': i, 'name': nombre}
        for i, nombre in enumerate(
            ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
             'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
            start=1
        )
    ]

    # construir filtros dinámicos
    filters = Q()
    if selected_year != 'all':
        filters &= Q(fecha_expedicion__year=selected_year)
    if selected_month != 'all':
        filters &= Q(fecha_expedicion__month=selected_month)
    if selected_type != 'TODOS':
        filters &= Q(tipo=selected_type)

    # query optimizada
    refrendos = (
        Refrendo.objects
        .filter(filters)
        .select_related('titulo', 'curso', 'creado_por')   # FK correctos
        .order_by('-fecha_expedicion')
    )

    # preparar datos para la tabla
    refrendos_data = []
    for r in refrendos:
        nombre_tc = (
            r.titulo.nombre if r.tipo == 'TITULO' and r.titulo
            else r.curso.nombre if r.tipo == 'CURSO' and r.curso
            else 'Sin dato'
        )
        refrendos_data.append({
            'nombre'      : nombre_tc,
            'persona'     : r.nombre_completo,
            'numero'      : r.numero_refrendo,
            'expedicion'  : r.fecha_expedicion.strftime('%d/%m/%Y') if r.fecha_expedicion else '',
            'vencimiento' : r.fecha_vencimiento.strftime('%d/%m/%Y') if r.fecha_vencimiento else '',
        })

    context = {
        'years'           : years,
        'months'          : months,
        'selected_year'   : selected_year,
        'selected_month'  : selected_month,
        'selected_type'   : selected_type,
        'refrendos'       : refrendos_data,
        'total_refrendos' : len(refrendos_data),
    }

    return render(request, 'estadisticas/estadisticas.html', context)


def detalle_refrendo(request, tipo, nombre):
    if tipo == 'TITULO':
        refrendos = Refrendo.objects.filter(titulo__nombre=nombre)
    else:
        refrendos = Refrendo.objects.filter(curso__nombre=nombre)
    
    context = {
        'refrendos': refrendos,
        'nombre': nombre,
        'tipo': tipo,
    }

    return render(request, 'estadisticas/detalle_refrendo.html', context)
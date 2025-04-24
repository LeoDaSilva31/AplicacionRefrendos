from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RefrendoForm
from .models import Refrendo, calcular_dias_habiles
from django.utils import timezone

# Listar todos los refrendos
@login_required
@permission_required('refrendos.ver_refrendo', raise_exception=True)
def refrendo_list(request):
    refrendos = Refrendo.objects.all()
    
    # Formatear las fechas a DD/MM/YYYY
    for refrendo in refrendos:
        if refrendo.fecha_vencimiento:
            refrendo.fecha_vencimiento = refrendo.fecha_vencimiento.strftime('%d/%m/%Y')
        if refrendo.fecha_expedicion:
            refrendo.fecha_expedicion = refrendo.fecha_expedicion.strftime('%d/%m/%Y')
        if refrendo.fecha_salida:
            refrendo.fecha_salida = refrendo.fecha_salida.strftime('%d/%m/%Y')
    
    return render(request, 'refrendos/refrendo_list.html', {'refrendos': refrendos})



# Agregar un nuevo refrendo
@login_required
@permission_required('refrendos.crear_refrendo', raise_exception=True)
def refrendo_add(request):
    if request.method == 'POST':
        form = RefrendoForm(request.POST, request.FILES)
        if form.is_valid():
            refrendo = form.save(commit=False)
            refrendo.creado_por = request.user  # Guarda el usuario que cargó el refrendo
            refrendo.save()
            return redirect('refrendos:refrendo-list')
    else:
        form = RefrendoForm()
    return render(request, 'refrendos/refrendo_form.html', {'form': form})


# Editar un refrendo existente
@login_required
@permission_required('refrendos.editar_refrendo', raise_exception=True)
def refrendo_edit(request, id):
    refrendo = get_object_or_404(Refrendo, id=id)
    
    # Si es un GET, no formateamos las fechas, ya que el formulario necesita los valores como objetos de fecha
    if request.method == 'GET':
        form = RefrendoForm(instance=refrendo)
    elif request.method == 'POST':
        form = RefrendoForm(request.POST, request.FILES, instance=refrendo)
        if form.is_valid():
            refrendo = form.save(commit=False)

            # Si se cargó la fecha_salida y la fecha_expedicion, calculamos automáticamente los días
            if refrendo.fecha_salida and refrendo.fecha_expedicion:
                refrendo.dias_corridos = (refrendo.fecha_salida - refrendo.fecha_expedicion).days
                refrendo.dias_habiles = calcular_dias_habiles(refrendo.fecha_expedicion, refrendo.fecha_salida)

            refrendo.save()
            return redirect('refrendos:refrendo-list')
    
    return render(request, 'refrendos/refrendo_form.html', {'form': form})




# Eliminar un refrendo
@login_required
@permission_required('refrendos.borrar_refrendo', raise_exception=True)
def refrendo_delete(request, id):
    refrendo = get_object_or_404(Refrendo, id=id)
    if request.method == 'POST':
        refrendo.delete()
        return redirect('refrendos:refrendo-list')
    return render(request, 'refrendos/refrendo_confirm_delete.html', {'refrendo': refrendo})


# Ver detalles de un refrendo
@login_required
@permission_required('refrendos.ver_refrendo', raise_exception=True)
def refrendo_detail(request, id):
    refrendo = get_object_or_404(Refrendo, id=id)
    
    # Formatear las fechas a DD/MM/YYYY
    if refrendo.fecha_vencimiento:
        refrendo.fecha_vencimiento = refrendo.fecha_vencimiento.strftime('%d/%m/%Y')
    if refrendo.fecha_expedicion:
        refrendo.fecha_expedicion = refrendo.fecha_expedicion.strftime('%d/%m/%Y')
    if refrendo.fecha_salida:
        refrendo.fecha_salida = refrendo.fecha_salida.strftime('%d/%m/%Y')
    
    return render(request, 'refrendos/refrendo_detail.html', {'refrendo': refrendo})



# Buscar refrendos
@login_required
@permission_required('refrendos.ver_refrendo', raise_exception=True)
def refrendo_search(request):
    query = request.GET.get('q', '')
    refrendos = Refrendo.objects.filter(nombre_completo__icontains=query) if query else []
    
    # Formatear las fechas a DD/MM/YYYY
    for refrendo in refrendos:
        if refrendo.fecha_vencimiento:
            refrendo.fecha_vencimiento = refrendo.fecha_vencimiento.strftime('%d/%m/%Y')
        if refrendo.fecha_expedicion:
            refrendo.fecha_expedicion = refrendo.fecha_expedicion.strftime('%d/%m/%Y')
        if refrendo.fecha_salida:
            refrendo.fecha_salida = refrendo.fecha_salida.strftime('%d/%m/%Y')
    
    return render(request, 'refrendos/refrendo_list.html', {
        'refrendos': refrendos,
        'query': query,
    })

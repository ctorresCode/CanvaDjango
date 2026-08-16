from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from evaluaciones.models import ArchivoTarea, Calificacion, Tarea

class MultipleFileInput(forms.FileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class TareaForm(forms.ModelForm):

    # Usamos nuestro nuevo campo personalizado
    archivos = MultipleFileField(
        required=False,
        label="Archivos adjuntos (puedes seleccionar varios)"
    )

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'curso', 'cantidad_puntos', 'Fecha_entrega']
        widgets = {
            'Fecha_entrega': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            )
        }

# Listar tareas
class ListarTareas(ListView):
    model = Tarea
    template_name = 'evaluacione/listaTareasMaestros.html'
    context_object_name = 'tareas'
    paginate_by = 5

    def get_queryset(self):
        tareas = Tarea.objects.all()
        return tareas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TareaForm()
        return context

# Crear tareas
class CrearTarea(CreateView):
    model = Tarea 
    template_name = 'evaluacione/crearTarea.html'
    form_class = TareaForm
    success_url = reverse_lazy('lista_de_tareas')

    def form_valid(self, form):
        tarea_creada = form.save()
        archivos = self.request.FILES.getlist('archivos')
        
        for archivo in archivos:
            ArchivoTarea.objects.create(tarea=tarea_creada, archivo=archivo)

        return super().form_valid(form)

# Detalle de la tarea
class DetalleTarea(DetailView):
    model = Tarea
    template_name = 'evaluacione/detalleTarea.html'
    context_object_name = 'tarea'

class EditarTarea(UpdateView):
    model = Tarea
    template_name = 'evaluacione/listaTareasMaestros.html' 
    form_class = TareaForm
    success_url = reverse_lazy('lista_de_tareas')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = Tarea.objects.all() 
        context['editando'] = True 
        return context  

class EliminarTarea(DeleteView):
    model = Tarea
    template_name = 'evaluacione/eliminarTarea.html'
    success_url = reverse_lazy('lista_de_tareas')

def ListaEntregas(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    entregas = Calificacion.objects.filter(tarea=tarea).select_related('estudiante__usuario').prefetch_related('archivos_adjuntos')

    if request.method == 'POST':
        entrega_id = request.POST.get('entrega_id')
        puntuacion = request.POST.get('puntuacion')
        retroalimentacion = request.POST.get('retroalimentacion')

        if entrega_id and puntuacion:
            entrega = get_object_or_404(Calificacion, id=entrega_id)
            entrega.puntuacion = puntuacion
            entrega.retroalimentacion = retroalimentacion
            entrega.save()

            messages.success(request, f'Calificación guardada')

    context = {
        'tarea': tarea,
        'entregas': entregas,
    }        

    return render(request, 'evaluacione/listaEntregas.html', context)    
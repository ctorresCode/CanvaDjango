from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from evaluaciones.models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'curso', 'cantidad_puntos', 'imagenes_relacionadas', 'Fecha_entrega']
        widgets = {
            'Fecha_entrega': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            )
        }

#Listar tareas
class ListarTareas(ListView):
    model = Tarea
    template_name = 'evaluacione/listaTareasMaestros.html'
    context_object_name = 'tareas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TareaForm()
        return context

#Crear tareas
class CrearTarea(CreateView):
    model = Tarea 
    template_name = 'evaluacione/crearTarea.html'
    form_class = TareaForm
    success_url = reverse_lazy('lista_de_tareas')

#detalle de la tarea
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
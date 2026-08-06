from django.contrib import messages
from django.http import JsonResponse, request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from academico import models
from academico.models import Curso, Inscripcion
from usuarios.models import Estudiante

# Create your views here.

#Gestionar los cursos como maestro
class CursoListView(ListView):
    model = Curso
    template_name = 'academi/curso_list.html'
    context_object_name = 'cursos'

#detalles de los cursos como maestro
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'academi/curso_detail.html'
    context_object_name = 'curso'

#creación de cursos como maestro
class CursoCreateView(CreateView):
    model = Curso
    template_name = 'academi/curso_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        form.instance.maestro = self.request.user.perfil_maestro
        return super().form_valid(form)

#Editar cursos como maestro
class CursoUpdateView(UpdateView):
    model = Curso
    template_name = 'academi/curso_update.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        form.instance.maestro = self.request.user.perfil_maestro
        return super().form_valid(form)


#Borrar cursos como maestro
class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'academi/curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')


#lista de cursos para inscribirse como estudiante
class ListaCursoEstudianteView(ListView):
    model = Curso
    template_name = 'academi/listacursoEstudianteInscripcion.html'
    context_object_name = 'cursos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            estudiante = self.request.user.perfil_estudiante
            context['cursos_inscritos_ids'] = list(
                Inscripcion.objects.filter(estudiante=estudiante)
                .values_list('curso_id', flat=True)
            )
        except Estudiante.DoesNotExist:
            context['cursos_inscritos_ids'] = []

        return context

class MisCursosEstudianteView(ListView):
    model = Curso
    template_name = 'academi/mis_cursos_estudiante.html'  
    context_object_name = 'cursos'

    def get_queryset(self):
        try:
            estudiante = self.request.user.perfil_estudiante
        except Estudiante.DoesNotExist:
            return Curso.objects.none()

        return Curso.objects.filter(estudiantes_inscritos__estudiante=estudiante) 

#Inscribirse al presionarm el boton logica
class InscribirCursoView(View):
        def post(self, request, id_curso):
            curso_solicitado = get_object_or_404(Curso, id=id_curso)
            try:
                estudiante_actual = request.user.perfil_estudiante
            except Estudiante.DoesNotExist:
                return JsonResponse(
                    {'mensaje': 'Solo los estudiantes pueden inscribirse a un curso.'},
                    status=403
                )
            
            inscripcion, creada = Inscripcion.objects.get_or_create(
                estudiante = estudiante_actual,
                curso = curso_solicitado
            )

            if creada:
                mensaje = (
                    f'¡Felicidades! Ya eres parte del curso "{curso_solicitado.nombre}" '
                    f'con el profesor {curso_solicitado.maestro}'
            )
            else:
                mensaje = 'Ya estabas inscrito en este curso.'

            return JsonResponse({'mensaje': mensaje, 'creada': creada})



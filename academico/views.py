from django.utils import timezone
from django.contrib import messages
from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EstudianteForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


from academico import models
from academico.models import Curso, Inscripcion
from evaluaciones.models import Calificacion, Tarea, ArchivoEntrega
from usuarios.models import Estudiante


# Gestionar los cursos como maestro
class CursoListView(ListView):
    model = Curso
    template_name = 'academi/curso_list.html'
    context_object_name = 'cursos'


# detalles de los cursos como maestro
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'academi/curso_detail.html'
    context_object_name = 'curso'


# creación de cursos como maestro
class CursoCreateView(CreateView):
    model = Curso
    template_name = 'academi/curso_form.html'
    fields = ['nombre', 'descripcion', 'imagen']
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        form.instance.maestro = self.request.user.perfil_maestro
        return super().form_valid(form)


# Editar cursos como maestro
class CursoUpdateView(UpdateView):
    model = Curso
    template_name = 'academi/curso_update.html'
    fields = ['nombre', 'descripcion', 'imagen']
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        form.instance.maestro = self.request.user.perfil_maestro
        return super().form_valid(form)


# Borrar cursos como maestro
class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'academi/curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')


# lista de cursos para inscribirse como estudiante
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


# Inscribirse al presionar el boton, lógica
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
            estudiante=estudiante_actual,
            curso=curso_solicitado
        )

        if creada:
            mensaje = (
                f'¡Felicidades! Ya eres parte del curso "{curso_solicitado.nombre}" '
                f'con el profesor {curso_solicitado.maestro}'
            )
        else:
            mensaje = 'Ya estabas inscrito en este curso.'

        return JsonResponse({'mensaje': mensaje, 'creada': creada})


class tableroEstudianteView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'academi/tablero_estudiante.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        try:
            estudiante = self.request.user.perfil_estudiante
        except Estudiante.DoesNotExist:
            return Tarea.objects.none()

        entregas = Calificacion.objects.filter(
            tarea=OuterRef('pk'),
            estudiante=estudiante
        )

        return Tarea.objects.filter(
            curso__estudiantes_inscritos__estudiante=estudiante
        ).select_related('curso').annotate(
            esta_entregada=Exists(entregas)
        ).order_by('Fecha_entrega').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ahora'] = timezone.now()
        return context


class DetalleTareaEstudianteView(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = 'academi/detalle_tarea_estudiante.html'
    context_object_name = 'tarea'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        try:
            estudiante = self.request.user.perfil_estudiante
        except Estudiante.DoesNotExist:
            return Tarea.objects.none()

        return Tarea.objects.filter(
            curso__estudiantes_inscritos__estudiante=estudiante
        ).select_related('curso').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            estudiante = self.request.user.perfil_estudiante
            entrega = Calificacion.objects.filter(
                tarea=self.object, estudiante=estudiante
            ).first()

            if entrega and (entrega.ruta_archivo or entrega.archivos_adjuntos.exists()):
                context['ruta_archivo'] = True
                context['puntuacion'] = entrega.puntuacion
            else:
                context['ruta_archivo'] = False
                context['puntuacion'] = None

            context['entrega'] = entrega
        except Estudiante.DoesNotExist:
            context['ruta_archivo'] = False
            context['puntuacion'] = None
            context['entrega'] = None

        context['ahora'] = timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        self.object = tarea_actual = self.get_object()

        if tarea_actual.Fecha_entrega and tarea_actual.Fecha_entrega < timezone.now():
            messages.error(request, "El plazo para entregar esta tarea ha expirado.")
            return redirect('detalle_tarea_estudiante', pk=tarea_actual.pk)

        try:
            estudiante_actual = request.user.perfil_estudiante
        except Estudiante.DoesNotExist:
            messages.error(request, "Solo los estudiantes registrados pueden entregar tareas.")
            return redirect('detalle_tarea_estudiante', pk=tarea_actual.pk)

        archivos_subidos = request.FILES.getlist('archivos')

        if archivos_subidos:
            entrega, created = Calificacion.objects.get_or_create(
                tarea=tarea_actual,
                estudiante=estudiante_actual,
            )

            for f in archivos_subidos:
                ArchivoEntrega.objects.create(entrega=entrega, archivo=f)

            messages.success(request, f"¡Se entregaron {len(archivos_subidos)} archivos con éxito!")
        else:
            messages.error(request, "Hubo un problema. Asegúrate de adjuntar al menos un archivo antes de enviar.")

        return redirect('detalle_tarea_estudiante', pk=tarea_actual.pk)

@login_required
def configuracion_perfil(request):
    perfil = request.user.perfil_estudiante

    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES, instance=perfil)
        
        if form.is_valid():
            form.save() 
            messages.success(request, "¡Tu perfil ha sido actualizado con éxito!")
            return redirect('configuracion_perfil') 
        else:
            messages.error(request, "Hubo un error al actualizar tu perfil. Por favor, revisa los datos ingresados.")    
    else:
        form = EstudianteForm(instance=perfil)

    return render(request, 'academi/settings_estudiante.html', {'form': form})
from django.db import models
from django.utils import timezone  
from tinymce.models import HTMLField
from academico.models import Curso
from usuarios.models import Estudiante


class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = HTMLField()
    cantidad_puntos = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='tareas')
    Fecha_entrega = models.DateTimeField(null=True, blank=True)

    @property
    def estado(self):
        if self.Fecha_entrega and self.Fecha_entrega < timezone.now():
            return 'Vencida'
        return 'Activa'

    def __str__(self):
        return self.titulo


class ArchivoTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='archivos_tareas/')

    def __str__(self):
        return f"Archivo de tarea: {self.tarea.titulo}"


class Calificacion(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='entregas')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='calificaciones')
    ruta_archivo = models.FileField(upload_to='entregas_estudiantes/', null=True, blank=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    puntuacion = models.IntegerField(null=True, blank=True)
    retroalimentacion = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('tarea', 'estudiante')

    def __str__(self):
        return f"Entrega de {self.estudiante.usuario.username} - {self.tarea.titulo}"


class ArchivoEntrega(models.Model):
    entrega = models.ForeignKey(Calificacion, on_delete=models.CASCADE, related_name='archivos_adjuntos')
    archivo = models.FileField(upload_to='entregas_estudiantes/multiples/')

    def __str__(self):
        return f"Adjunto de {self.entrega.estudiante.usuario.username} - {self.entrega.tarea.titulo}"
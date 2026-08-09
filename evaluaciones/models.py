from django.db import models
from pytz import timezone
from tinymce.models import HTMLField
from academico.models import Curso

# Create your models here.
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
        return f"Archivo para: {self.tarea.titulo}"


from django.db import models
from pytz import timezone

from academico.models import Curso

# Create your models here.
class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    cantidad_puntos = models.IntegerField()
    imagenes_relacionadas = models.ImageField(upload_to='imagenes_tareas/', blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='tareas')
    Fecha_entrega = models.DateTimeField(null=True, blank=True)

    @property
    def estado(self):
        if self.Fecha_entrega and self.Fecha_entrega < timezone.now():
            return 'Vencida'
        return 'Activa'

    def __str__(self):
        return self.titulo    
         
    

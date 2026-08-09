from django.db import models

from usuarios.models import Estudiante, Maestro

# Create your models here.
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='cursos/', null=True, blank=True)
    maestro = models.ForeignKey(Maestro, on_delete=models.CASCADE, related_name='cursos_impartidos')
    
    def __str__(self):
        return self.nombre

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estudiantes_inscritos')
    
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.usuario.username} -> {self.curso.nombre}"

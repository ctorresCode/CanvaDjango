from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):

    email = models.EmailField('correo electronico',unique=True)
    username = None
    Roles = (
        ('Estudiante', 'estudiante'),
        ('Profesor', 'profesor'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    rol = models.CharField(max_length=20, choices=Roles, default='Estudiante')

    def __str__(self):
        return self.email

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_estudiante')
    edad = models.PositiveIntegerField(null=True, blank=True)
    descripcion_personal = models.TextField(blank=True)

    def __str__(self):
        return f"Estudiante: {self.usuario.get_full_name() or self.usuario.email}"

class Maestro(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_maestro')
    edad = models.PositiveIntegerField(null=True, blank=True)
    informacion_profesional = models.TextField(blank=True)

    def __str__(self):
        return f"Maestro: {self.usuario.get_full_name() or self.usuario.username}" 
       


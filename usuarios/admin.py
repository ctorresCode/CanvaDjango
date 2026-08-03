from django.contrib import admin

from usuarios.models import Estudiante, Maestro, Usuario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Maestro)

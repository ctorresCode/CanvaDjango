from django import forms
from usuarios.models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['edad', 'descripcion_personal', 'imagen_perfil']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from evaluaciones.models import ComentarioEntrega
from usuarios.models import Estudiante, Usuario


class RegistrarUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'rol')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None   


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioEntrega
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Agregar un comentario...'
            }),
        }

    
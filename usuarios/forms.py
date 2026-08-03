
from django.contrib.admin import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario


class RegistrarUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'rol')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None   
    
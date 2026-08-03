from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, TemplateView
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from usuarios.models import Estudiante, Maestro

# Create your views here.
class RegistroUsuarioView(CreateView):
    template_name = 'usuario/registro.html'
    form_class = RegistrarUsuarioForm
    success_url = reverse_lazy('despachador_roles')

    def form_valid(self, form):
        usuario = form.save()
        if usuario.rol == 'Estudiante':
            Estudiante.objects.create(usuario=usuario)
        elif usuario.rol == 'Profesor':
            Maestro.objects.create(usuario=usuario)
    
        login(self.request, usuario)
        return super().form_valid(form)

class DespachadorRolesView(LoginRequiredMixin, RedirectView):
    """
    Evalúa el rol del usuario logueado y calcula la URL correcta.
    """
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.rol == 'Estudiante':
            return reverse_lazy('panel_estudiante')
        elif self.request.user.rol == 'Profesor':
            return reverse_lazy('panel_maestro')
        return reverse_lazy('admin:index')
    
class EsEstudianteMixin(AccessMixin):
    """Permite el paso solo si es Estudiante. Si es Maestro, lo rebota a su panel."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() 
        
        if request.user.rol != 'Estudiante':
            return redirect('panel_maestro') 
            
        return super().dispatch(request, *args, **kwargs)    

class EsProfesorMixin(AccessMixin):
    """Permite el paso solo si es Profesor. Si es Estudiante, lo rebota a su panel."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
            
        if request.user.rol != 'Profesor':
            return redirect('panel_estudiante') 
            
        return super().dispatch(request, *args, **kwargs)

class PanelEstudianteView(EsEstudianteMixin, TemplateView):
    template_name = 'usuario/panel_estudiante.html'

class PanelMaestroView(EsProfesorMixin, TemplateView):
    template_name = 'usuario/panel_maestro.html'

class InvitadoView(TemplateView):
    template_name = 'usuario/invitado.html'

def cerrar_sesion(request):
    logout(request)
    return redirect('Invitado')  

   
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from usuarios.views import DespachadorRolesView, InvitadoView, PanelEstudianteView, PanelMaestroView, RegistroUsuarioView

urlpatterns = [
    path('', InvitadoView.as_view(), name='Invitado'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('login/', LoginView.as_view(template_name='usuario/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DespachadorRolesView.as_view(), name='despachador_roles'),
    path('panel-estudiante/', PanelEstudianteView.as_view(), name='panel_estudiante'),
    path('panel-maestro/', PanelMaestroView.as_view(), name='panel_maestro'),
]

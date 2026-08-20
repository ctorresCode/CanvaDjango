from usuarios.models import Estudiante

def estudiante_actual(request):
    estudiante = None
    if request.user.is_authenticated:
        try:
            estudiante = request.user.perfil_estudiante
        except Estudiante.DoesNotExist:
            estudiante = None
    return {'estudiante_actual': estudiante}
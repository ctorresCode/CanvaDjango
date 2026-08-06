from django.urls import include, path

from academico.views import CursoCreateView, CursoDeleteView, CursoDetailView, CursoListView, CursoUpdateView, InscribirCursoView, ListaCursoEstudianteView, MisCursosEstudianteView

urlpatterns = [
    path('panel-maestro/academico/', CursoListView.as_view(), name='curso_list'),
    path('panel-maestro/academico/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('panel-maestro/academico/crear_materia/', CursoCreateView.as_view(), name='curso_create'),
    path('panel-maestro/academico/editar_materia/<int:pk>/', CursoUpdateView.as_view(), name='curso_update'),
    path('panel-maestro/academico/eliminar_materia/<int:pk>/', CursoDeleteView.as_view(), name='curso_delete'),
    
    #desde el panel del estudiante, inscribirse a un curso
    path('panel-estudiante/academico/', ListaCursoEstudianteView.as_view(), name='lista_curso_estudiante_inscripcion'),
    path('panel-estudiante/academico/lista_cursos/inscribirse/<int:id_curso>/', InscribirCursoView.as_view(), name='inscribir_curso'),

    #desde el panel del estudiante, ver los cursos en los que ya está inscrito
    path('panel-estudiante/academico/mis-cursos/', MisCursosEstudianteView.as_view(), name='lista_curso_estudiante'),

]

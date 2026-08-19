from django.urls import include, path

from academico.views import CursoCreateView, CursoDeleteView, CursoDetailView, CursoListView, CursoUpdateView, DetalleTareaEstudianteView, EstudiantePresionaCursoInscrito, InscribirCursoView, ListaCursoEstudianteView, MisCursosEstudianteView, agregarComentario, muestraEstudiantePorCurso, tableroEstudianteView, configuracion_perfil

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
    path('panel-estudiante/academico/tablero/', tableroEstudianteView.as_view(), name='tablero_estudiante'),
    path('panel-estudiante/academico/tablero/curso/<int:pk>/', EstudiantePresionaCursoInscrito.as_view(), name='tablero_estudiante_curso'),
    path('panel-estudiante/academico/tablero/curso/<int:curso_id>/personas/', muestraEstudiantePorCurso, name='muestra_estudiantes_por_curso'),
    path('panel-estudiante/academico/settings/', configuracion_perfil, name='configuracion_perfil'),
    path('panel-estudiante/academico/inscritos/', EstudiantePresionaCursoInscrito.as_view(), name='estudiante_presiona_curso_inscrito'),

    #detalle de la tarea desde el panel del estudiante
    path('panel-estudiante/academico/tablero/tarea/<int:pk>/', DetalleTareaEstudianteView.as_view(),name='detalle_tarea_estudiante'),
    path('academico/entrega/<int:entrega_id>/comentar/', agregarComentario, name='agregar_comentario')


]

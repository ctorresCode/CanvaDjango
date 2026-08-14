from django.urls import path

from evaluaciones.views import CrearTarea, DetalleTarea, EditarTarea, EliminarTarea, ListaEntregas, ListarTareas


urlpatterns = [
    path('panel-maestro/evaluaciones/lista_tareas/', ListarTareas.as_view(), name='lista_de_tareas'),
    path('panel-maestro/evaluaciones/crear_tarea/', CrearTarea.as_view(), name='crear_tarea'),
    path('panel-maestro/evaluaciones/lista_tareas/<int:pk>/', DetalleTarea.as_view(), name='detalle_tarea'),
    path('panel-maestro/evaluaciones/editar_tareas/<int:pk>/', EditarTarea.as_view(), name='editar_tarea'),
    path('panel-maestro/evaluaciones/eliminar_tareas/<int:pk>/', EliminarTarea.as_view(), name='eliminar_tarea'),
    path('panel-maestro/evaluaciones/entrega/<tarea_id>/', ListaEntregas, name='lista_entregas'),
]


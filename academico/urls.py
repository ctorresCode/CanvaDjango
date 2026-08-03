from django.urls import include, path

from academico.views import CursoCreateView, CursoDeleteView, CursoDetailView, CursoListView, CursoUpdateView

urlpatterns = [
    path('panel-maestro/academico/', CursoListView.as_view(), name='curso_list'),
    path('panel-maestro/academico/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('panel-maestro/academico/crear_materia/', CursoCreateView.as_view(), name='curso_create'),
    path('panel-maestro/academico/editar_materia/<int:pk>/', CursoUpdateView.as_view(), name='curso_update'),
    path('panel-maestro/academico/eliminar_materia/<int:pk>/', CursoDeleteView.as_view(), name='curso_delete'),
]

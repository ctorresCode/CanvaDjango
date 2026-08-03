from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from academico.models import Curso

# Create your views here.

#Gestionar los cursos
class CursoListView(ListView):
    model = Curso
    template_name = 'academi/curso_list.html'
    context_object_name = 'cursos'

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'academi/curso_detail.html'
    context_object_name = 'curso'

class CursoCreateView(CreateView):
    model = Curso
    template_name = 'academi/curso_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        form.instance.maestro = self.request.user.perfil_maestro
        return super().form_valid(form)

class CursoUpdateView(UpdateView):
    model = Curso
    template_name = 'academi/curso_update.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        form.instance.maestro = self.request.user.perfil_maestro
        return super().form_valid(form)

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'academi/curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')

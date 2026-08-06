
from django.db.models.signals import post_save
from django.dispatch import receiver
from evaluaciones.models import Tarea

@receiver(post_save, sender=Tarea)
def tarea_guardada(sender, instance, created, **kwargs):
    if created:
        print(f"Se ha creado una nueva tarea: {instance.titulo}")
    else:
        print(f"Se ha actualizado la tarea: {instance.titulo}")
             
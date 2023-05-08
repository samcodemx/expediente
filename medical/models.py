from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.IntegerField()

class Valoracion(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    medico = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
from django.contrib import admin
from .models import Medico, Paciente, HistoriaClinica, Antecedentes, PadecimientoActual, ExploracionFisica, Consulta

# Register your models here.
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(HistoriaClinica)
admin.site.register(Antecedentes)
admin.site.register(PadecimientoActual)
admin.site.register(ExploracionFisica)
admin.site.register(Consulta)

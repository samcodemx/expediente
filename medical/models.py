from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User, AbstractUser

# Create your models here.
class Medico(models.Model):
    PREFIJO_CHOICES = [
        ('dr', 'Dr.'),
        ('dr', 'Dra.'),
        ('lic', 'Lic.'),
    ]
    ESPECIALIDAD_CHOICES = [
        ('medico_gral', 'Medicina General'),
        ('fisio', 'Fisioterapia'),
    ]
    cedula = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medico', null=True)
    nombre = models.CharField(max_length=100)
    apellido_pat = models.CharField(max_length=50)
    apellido_mat = models.CharField(max_length=50)
    prefijo = models.CharField(max_length=5, choices=PREFIJO_CHOICES)
    especialidad = models.CharField(max_length=20, choices=ESPECIALIDAD_CHOICES)
    universidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellido_pat

class Paciente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERO', 'Soltero'),
        ('CASADO', 'Casado'),
        ('UNION_LIBRE', 'Union libre'),
        ('DIVORCIADO', 'Divorciado'),
        ('VIUDO', 'Viudo'),
    ]

    GRUPO_RH_CHOICES = [
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('O+', 'O+'),
        ('AB+', 'AB+'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('O-', 'O-'),
        ('AB-', 'AB-'),
        ('DESC', 'Desconocido'),
    ]

    ESCOLARIDAD_CHOICES = [
        ('NINGUNA', 'Ninguna'),
        ('PRIMARIA', 'Primaria'),
        ('PRIMARIA_T', 'Primaria Trunca'),
        ('SECUNDARIA', 'Secundaria'),
        ('SECUNDARIA_T', 'Secundaria Trunca'),
        ('PREPARATORIA', 'Preparatoria'),
        ('PREPARATORIA_T', 'Preparatoria Trunca'),
        ('TECNICO', 'Carrera Tecnica'),
        ('TECNICO_T', 'Carrera Tecnica Trunca'),
        ('LICENCIATURA', 'Licenciatura'),
        ('LICENCIATURA_T', 'Licenciatura Trunca'),
        ('SUPERIOR', 'Superior'),
    ]
    
    nombre = models.CharField(max_length=50)
    apellido_pat = models.CharField(max_length=50)
    apellido_mat = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_CHOICES)
    grupo_rh = models.CharField(max_length=4, choices=GRUPO_RH_CHOICES)
    alergias = models.CharField(max_length=30)
    curp = models.CharField(max_length=18, blank=True, null=True)
    nacionalidad = models.CharField(max_length=20, blank=True, null=True)
    escolaridad = models.CharField(max_length=30, choices=ESCOLARIDAD_CHOICES, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ocupacion = models.CharField(max_length=50, blank=True, null=True)
    empleador = models.CharField(max_length=100, blank=True, null=True)
    telefono_personal = models.CharField(max_length=50, blank=True, null=True)
    nombre_contacto_emergencia = models.CharField(max_length=100, blank=True, null=True)
    telefono_contacto_emergencia = models.CharField(max_length=20, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellido_pat + ' ' + self.apellido_mat

class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.paciente) + ' por ' + str(self.medico) + ' - ' + str(self.fecha)

    class Meta:
            verbose_name = "Historia Clínica"
            verbose_name_plural = "1.Historias Clinicas"

class Antecedentes(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    ahf = models.TextField()
    apnp = models.TextField()
    app = models.TextField()
    ago = models.TextField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.historia_clinica.paciente) + ' por ' + str(self.medico) + ' - ' + str(self.fecha)
    
    class Meta:
            verbose_name = "Antecedentes"
            verbose_name_plural = "2.Antecedentes"

class PadecimientoActual(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    padecimiento_actual = models.TextField()
    piel_tegumentos = models.TextField()
    cabeza_cuello  = models.TextField()
    torax = models.TextField()
    abdomen = models.TextField()
    genitourinario  = models.TextField()
    musculo_extremidades = models.TextField()
    neurologico = models.TextField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.historia_clinica.paciente) + ' por ' + str(self.medico) + ' - ' + str(self.fecha)

    class Meta:
            verbose_name = "Padecimiento Actual"
            verbose_name_plural = "3.Padecimientos Actuales"

class ExploracionFisica(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    temperatura = models.DecimalField(max_digits=5, decimal_places=1)
    presion_arterial = models.CharField(max_length=20)
    frecuencia_cardiaca = models.IntegerField()
    frecuencia_respiratoria = models.IntegerField()
    saturacion_oxigeno = models.IntegerField()
    peso = models.FloatField()
    talla = models.FloatField()
    imc = models.FloatField()
    glucosa = models.FloatField()
    descripcion_exploracion = models.TextField()
    # aspectos_generales = models.TextField()
    # piel_tegumentos = models.TextField()
    # cabeza_cuello = models.TextField()
    # torax = models.TextField()
    # abdomen_pelvis = models.TextField()
    # extremidades = models.TextField()
    # neurologico = models.TextField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.historia_clinica.paciente) + ' por ' + str(self.medico) + ' - ' + str(self.fecha)

    class Meta:
        verbose_name = "Exploracion Física"
        verbose_name_plural = "4.Exploraciones Físicas"


#Pendiente la implementacion de subida de archivos
# class Study(models.Model):
#     record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
#     date = models.DateField()
#     description = models.TextField()
#     test_results = models.TextField()
#     image_path = models.CharField(max_length=200)
#     conclusion = models.TextField()
#     recommendations = models.TextField()
    # Add any other relevant fields for the Study model

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    diagnostico = models.CharField(max_length=100)
    folio_receta = models.IntegerField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Consulta a ' + str(self.paciente) + ' por ' + str(self.medico) + ' - ' + str(self.fecha)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "5.Consultas"

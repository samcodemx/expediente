# Generated by Django 4.2.1 on 2023-05-23 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoriaClinica",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateField()),
                ("notas", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Medico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("apellido_pat", models.CharField(max_length=50)),
                ("apellido_mat", models.CharField(max_length=50)),
                (
                    "prefijo",
                    models.CharField(
                        choices=[("dr", "Dr."), ("dr", "Dra."), ("lic", "Lic.")],
                        max_length=5,
                    ),
                ),
                (
                    "especialidad",
                    models.CharField(
                        choices=[
                            ("medico_gral", "Medicina General"),
                            ("fisio", "Fisioterapia"),
                        ],
                        max_length=20,
                    ),
                ),
                ("universidad", models.CharField(max_length=100)),
                ("telefono", models.CharField(blank=True, max_length=20)),
                (
                    "cedula",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medico",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Paciente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=50)),
                ("apellido_pat", models.CharField(max_length=50)),
                ("apellido_mat", models.CharField(max_length=50)),
                ("fecha_nacimiento", models.DateField()),
                (
                    "genero",
                    models.CharField(
                        choices=[("M", "Masculino"), ("F", "Femenino")], max_length=10
                    ),
                ),
                (
                    "estado_civil",
                    models.CharField(
                        choices=[
                            ("soltero", "Soltero"),
                            ("casado", "Casado"),
                            ("union_libre", "Union libre"),
                            ("divorciado", "Divorciado"),
                            ("viudo", "Viudo"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "grupo_rh",
                    models.CharField(
                        choices=[
                            ("a+", "A+"),
                            ("b+", "B+"),
                            ("o+", "O+"),
                            ("ab+", "AB+"),
                            ("a-", "A-"),
                            ("b-", "B-"),
                            ("o-", "O-"),
                            ("ab-", "AB-"),
                            ("desc", "Desconocido"),
                        ],
                        max_length=4,
                    ),
                ),
                ("alergias", models.CharField(max_length=30)),
                ("nacionalidad", models.CharField(max_length=20)),
                (
                    "escolaridad",
                    models.CharField(
                        choices=[
                            ("ninguna", "Ninguna"),
                            ("primaria", "Primaria"),
                            ("primaria_t", "Primaria Trunca"),
                            ("secundaria", "Secundaria"),
                            ("secundaria_t", "Secundaria Trunca"),
                            ("preparatoria", "Preparatoria"),
                            ("preparatoria_t", "Preparatoria Trunca"),
                            ("tecnico", "Carrera Tecnica"),
                            ("tecnico_t", "Carrera Tecnica Trunca"),
                            ("licenciatura", "Licenciatura"),
                            ("licenciatura_t", "Licenciatura Trunca"),
                            ("superior", "Superior"),
                        ],
                        max_length=30,
                    ),
                ),
                ("religion", models.CharField(max_length=50)),
                ("direccion", models.CharField(max_length=200)),
                ("ocupacion", models.CharField(max_length=50)),
                ("empleador", models.CharField(max_length=100)),
                ("telefono_personal", models.CharField(max_length=50)),
                ("nombre_contacto_emergencia", models.CharField(max_length=100)),
                ("telefono_contacto_emergencia", models.CharField(max_length=20)),
                ("notas", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PadecimientoActual",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateTimeField()),
                ("padecimiento_actual", models.TextField()),
                ("piel_tegumentos", models.TextField()),
                ("cabeza_cuello", models.TextField()),
                ("torax", models.TextField()),
                ("abdomen", models.TextField()),
                ("genitourinario", models.TextField()),
                ("musculo_extremidades", models.TextField()),
                ("neurologico", models.TextField()),
                ("notas", models.TextField(blank=True, null=True)),
                (
                    "historia_clinica",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical.historiaclinica",
                    ),
                ),
                (
                    "medico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="medical.medico"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="historiaclinica",
            name="medico",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="medical.medico"
            ),
        ),
        migrations.AddField(
            model_name="historiaclinica",
            name="paciente",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="medical.paciente"
            ),
        ),
        migrations.CreateModel(
            name="ExploracionFisica",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateTimeField()),
                ("temperatura", models.DecimalField(decimal_places=1, max_digits=5)),
                ("presion_arterial", models.CharField(max_length=20)),
                ("frecuencia_cardiaca", models.IntegerField()),
                ("frecuencia_respiratoria", models.IntegerField()),
                ("saturacion_oxigeno", models.IntegerField()),
                ("peso", models.FloatField()),
                ("talla", models.FloatField()),
                ("imc", models.FloatField()),
                ("glucosa", models.FloatField()),
                ("aspectos_generales", models.TextField()),
                ("piel_tegumentos", models.TextField()),
                ("cabeza_cuello", models.TextField()),
                ("torax", models.TextField()),
                ("abdomen_pelvis", models.TextField()),
                ("extremidades", models.TextField()),
                ("neurologico", models.TextField()),
                ("notas", models.TextField(blank=True, null=True)),
                (
                    "medico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="medical.medico"
                    ),
                ),
                (
                    "padecimiento_actual",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical.padecimientoactual",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Consulta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateField()),
                ("diagnostico", models.CharField(max_length=100)),
                ("folio_receta", models.IntegerField()),
                ("notas", models.TextField(blank=True, null=True)),
                (
                    "medico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="medical.medico"
                    ),
                ),
                (
                    "paciente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical.paciente",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Antecedentes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateField()),
                ("ahf", models.TextField()),
                ("apnp", models.TextField()),
                ("app", models.TextField()),
                ("ago", models.TextField()),
                ("notas", models.TextField(blank=True, null=True)),
                (
                    "historia_clinica",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical.historiaclinica",
                    ),
                ),
                (
                    "medico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="medical.medico"
                    ),
                ),
            ],
        ),
    ]

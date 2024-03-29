# Generated by Django 4.2.2 on 2023-06-07 04:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("medical", "0011_alter_paciente_estado_civil_alter_paciente_grupo_rh"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paciente",
            name="apellido_mat",
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="apellido_pat",
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="escolaridad",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NINGUNA", "NINGUNA"),
                    ("PRIMARIA", "PRIMARIA"),
                    ("PRIMARIA_T", "PRIMARIA TRUNCA"),
                    ("SECUNDARIA", "SECUNDARIA"),
                    ("SECUNDARIA_T", "SECUNDARIA TRUNCA"),
                    ("PREPARATORIA", "PREPARATORIA"),
                    ("PREPARATORIA_T", "PREPARATORIA TRUNCA"),
                    ("TECNICO", "CARRERA TECNICA"),
                    ("TECNICO_T", "CARRERA TECNICA TRUNCA"),
                    ("LICENCIATURA", "LICENCIATURA"),
                    ("LICENCIATURA_T", "LICENCIATURA TRUNCA"),
                    ("SUPERIOR", "SUPERIOR"),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="estado_civil",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SOLTERO", "SOLTERO"),
                    ("CASADO", "CASADO"),
                    ("UNION_LIBRE", "UNION LIBRE"),
                    ("DIVORCIADO", "DIVORCIADO"),
                    ("VIUDO", "VIUDO"),
                ],
                max_length=15,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="grupo_rh",
            field=models.CharField(
                choices=[
                    ("A+", "A+"),
                    ("B+", "B+"),
                    ("O+", "O+"),
                    ("AB+", "AB+"),
                    ("A-", "A-"),
                    ("B-", "B-"),
                    ("O-", "O-"),
                    ("AB-", "AB-"),
                    ("DESC", "DESCONOCIDO"),
                ],
                default="DESC",
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="nombre",
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="telefono_contacto_emergencia",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="telefono_personal",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

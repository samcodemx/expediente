# Generated by Django 4.2.2 on 2023-06-07 07:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("medical", "0012_alter_paciente_apellido_mat_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="antecedentes",
            name="ago",
            field=models.TextField(blank=True, null=True),
        ),
    ]

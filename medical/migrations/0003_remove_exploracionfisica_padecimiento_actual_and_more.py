# Generated by Django 4.2.1 on 2023-05-23 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("medical", "0002_remove_exploracionfisica_abdomen_pelvis_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="exploracionfisica",
            name="padecimiento_actual",
        ),
        migrations.AddField(
            model_name="exploracionfisica",
            name="historia_clinica",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                to="medical.historiaclinica",
            ),
            preserve_default=False,
        ),
    ]
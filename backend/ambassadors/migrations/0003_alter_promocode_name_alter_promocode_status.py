# Generated by Django 4.2.10 on 2024-03-03 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ambassadors", "0002_alter_merchandiseshippingrequest_options_promocode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="promocode",
            name="name",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Промокод"
            ),
        ),
        migrations.AlterField(
            model_name="promocode",
            name="status",
            field=models.CharField(
                choices=[("active", "Активный"), ("inactive", "Неактивный")],
                default="active",
                max_length=10,
                verbose_name="Статус промокода",
            ),
        ),
    ]

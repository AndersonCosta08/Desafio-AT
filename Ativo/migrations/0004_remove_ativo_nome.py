# Generated by Django 5.1 on 2024-08-29 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Ativo", "0003_alter_ativo_periodicidade"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ativo",
            name="nome",
        ),
    ]

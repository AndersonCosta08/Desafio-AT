# Generated by Django 5.1 on 2024-08-28 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Ativo", "0002_alter_ativo_periodicidade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ativo",
            name="periodicidade",
            field=models.IntegerField(),
        ),
    ]

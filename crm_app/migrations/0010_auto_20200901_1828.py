# Generated by Django 3.0.8 on 2020-09-01 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0009_auto_20200901_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='servicefee',
            field=models.IntegerField(default=33),
        ),
    ]

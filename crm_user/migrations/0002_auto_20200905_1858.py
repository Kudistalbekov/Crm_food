# Generated by Django 3.0.8 on 2020-09-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]

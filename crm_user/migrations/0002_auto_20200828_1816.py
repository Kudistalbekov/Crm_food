# Generated by Django 3.0.8 on 2020-08-28 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='is_active',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='myuser',
            old_name='is_admin',
            new_name='admin',
        ),
        migrations.RenameField(
            model_name='myuser',
            old_name='is_staff',
            new_name='staff',
        ),
        migrations.RenameField(
            model_name='myuser',
            old_name='is_superuser',
            new_name='superuser',
        ),
    ]
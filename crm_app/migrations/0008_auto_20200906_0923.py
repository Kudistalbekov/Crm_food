# Generated by Django 3.0.8 on 2020-09-06 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0007_auto_20200906_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='crm_app.Table'),
        ),
    ]

# Generated by Django 3.0.8 on 2020-09-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='totalsum',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='meal',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='waiter_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='orderedmeal',
            name='count',
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='orderedmeal',
            name='total_sum',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
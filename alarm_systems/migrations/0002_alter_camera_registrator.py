# Generated by Django 4.1.3 on 2022-12-11 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alarm_systems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='registrator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='alarm_systems.registrator'),
        ),
    ]

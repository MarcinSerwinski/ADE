# Generated by Django 4.1.3 on 2022-12-08 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Central',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=80, null=True)),
                ('phone_number', models.CharField(max_length=24, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_systems.customer')),
            ],
        ),
        migrations.CreateModel(
            name='SystemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_installed', models.DateField(auto_now_add=True)),
                ('last_check', models.DateField(auto_now=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_systems.location')),
                ('system_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_systems.systemtype')),
            ],
        ),
        migrations.CreateModel(
            name='Registrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('system_types', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_systems.system')),
            ],
        ),
        migrations.CreateModel(
            name='MotionSensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('placement', models.IntegerField(choices=[(1, 'Zewnętrzny'), (2, 'Wewnętrzny')], default=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('central', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_systems.central')),
            ],
        ),
        migrations.AddField(
            model_name='central',
            name='system_types',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_systems.system'),
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('placement', models.IntegerField(choices=[(1, 'Zewnętrzna'), (2, 'Wewnętrzna')], default=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('registrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alarm_systems.registrator')),
            ],
        ),
    ]

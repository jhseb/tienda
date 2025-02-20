# Generated by Django 5.1.4 on 2025-01-22 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('cedula', models.IntegerField(max_length=20, primary_key=True, serialize=False, verbose_name='Cédula')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono')),
                ('direccion', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('rol', models.IntegerField(verbose_name='Rol')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Nombre de Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100, verbose_name='título producto')),
                ('imagen', models.ImageField(null=True, upload_to='myapp/static/imagenes/', verbose_name='imagen producto')),
                ('descripcion', models.TextField(null=True, verbose_name='descripción producto')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='precio producto')),
                ('cantidad', models.IntegerField(default=0, verbose_name='cantidad producto')),
                ('marca', models.CharField(blank=True, max_length=50, null=True, verbose_name='marca producto')),
            ],
        ),
        migrations.CreateModel(
            name='carrito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idproducto', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('estado', models.CharField(default='por comprar', max_length=20, verbose_name='Estado')),
                ('car_cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('cedula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.cliente', verbose_name='Cliente')),
            ],
        ),
    ]

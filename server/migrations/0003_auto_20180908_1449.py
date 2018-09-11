# Generated by Django 2.0.8 on 2018-09-08 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_finger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Faces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonArrival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('come_in', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Device')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Person')),
            ],
        ),
        migrations.RemoveField(
            model_name='finger',
            name='finger_hash',
        ),
        migrations.AddField(
            model_name='finger',
            name='finger_num',
            field=models.BigIntegerField(null=True, unique=True),
        ),
    ]

# Generated by Django 2.0.8 on 2018-09-10 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_auto_20180909_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonUnauthorizedEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Device', verbose_name='Устройство')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Person', verbose_name='ФИО')),
            ],
            options={
                'verbose_name': 'История несанкционированных входов',
                'verbose_name_plural': 'История несанкционированных входов',
            },
        ),
    ]

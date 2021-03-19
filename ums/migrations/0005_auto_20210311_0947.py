# Generated by Django 3.1.1 on 2021-03-11 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ums', '0004_auto_20210311_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='password',
            field=models.CharField(max_length=300, unique=True, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(max_length=90, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='receptionist',
            name='password',
            field=models.CharField(max_length=300, unique=True, verbose_name='Password'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-13 10:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import libraries.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('operators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=libraries.models.content_file_name)),
                ('type', models.CharField(max_length=50)),
                ('script', models.TextField()),
                ('visibility', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operators.Operator')),
            ],
            options={
                'ordering': ['-timestamp', '-update'],
            },
        ),
    ]

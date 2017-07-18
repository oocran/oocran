# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-18 02:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=120)),
                ('vendor_id', models.CharField(max_length=4)),
                ('product_id', models.CharField(max_length=4)),
                ('is_assigned', models.BooleanField(default=False)),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=120)),
                ('name', models.CharField(max_length=120)),
                ('cpu', models.CharField(max_length=120)),
                ('ram', models.CharField(max_length=120)),
                ('disc', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('priority', models.IntegerField()),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('type', models.CharField(max_length=120)),
                ('ip', models.CharField(max_length=120)),
                ('sdn_controller', models.CharField(blank=True, max_length=120, null=True)),
                ('latitude', models.FloatField(max_length=120)),
                ('longitude', models.FloatField(max_length=120)),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aws',
            fields=[
                ('vim_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vims.Vim')),
                ('access_key_id', models.CharField(max_length=120)),
                ('secret_access_key', models.CharField(max_length=120)),
                ('session_token', models.CharField(max_length=120)),
                ('keypair_name', models.CharField(max_length=120)),
            ],
            bases=('vims.vim',),
        ),
        migrations.CreateModel(
            name='Azure',
            fields=[
                ('vim_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vims.Vim')),
                ('tenant_id', models.CharField(max_length=120)),
                ('client_id', models.CharField(max_length=120)),
                ('client_secret', models.CharField(max_length=120)),
                ('subscription_id', models.CharField(max_length=120)),
            ],
            bases=('vims.vim',),
        ),
        migrations.CreateModel(
            name='Gce',
            fields=[
                ('vim_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vims.Vim')),
                ('google_project_id', models.CharField(max_length=120)),
                ('google_client_email', models.CharField(max_length=120)),
                ('google_json_key_location', models.CharField(max_length=120)),
            ],
            bases=('vims.vim',),
        ),
        migrations.CreateModel(
            name='OpenStack',
            fields=[
                ('vim_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vims.Vim')),
                ('username', models.CharField(default='admin', max_length=120)),
                ('version', models.IntegerField(default=3)),
                ('password', models.CharField(max_length=120)),
                ('project_domain', models.CharField(default='default', max_length=120)),
                ('project', models.CharField(default='admin', max_length=120)),
                ('public_network', models.CharField(max_length=120)),
                ('domain', models.CharField(default='default', max_length=120)),
            ],
            bases=('vims.vim',),
        ),
        migrations.AddField(
            model_name='node',
            name='vim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vims.Vim'),
        ),
        migrations.AddField(
            model_name='device',
            name='vim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vims.Vim'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-31 06:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('client_secret', models.UUIDField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('scope_name', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('scope_info', models.TextField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Grant_token',
            fields=[
                ('grant_id', models.AutoField(primary_key=True, serialize=False)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('scope', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauthprovider.scope')),
            ],
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-05 02:01

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauthprovider', '0011_alter_client_client_secret_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='authorization_code_expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 9, 6, 46, 655040, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_secret',
            field=models.UUIDField(default=uuid.UUID('cfa11040-cbcf-4eca-8a8d-0260b0dd6aae'), unique=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='authorization_code',
            field=models.UUIDField(default=uuid.UUID('adcaa51c-45ec-457c-afd5-c94c502c4fcc'), null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 15, 1, 46, 639092, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='token',
            name='token_body',
            field=models.UUIDField(default=uuid.UUID('d9dad7ae-164a-488c-98f7-35e447710af6')),
        ),
    ]

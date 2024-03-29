# Generated by Django 5.0.1 on 2024-02-04 09:23

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauthprovider', '0010_alter_client_client_secret_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_secret',
            field=models.UUIDField(default=uuid.UUID('97ec968a-a695-459e-b0b6-85b0e2758a9f'), unique=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='authorization_code',
            field=models.UUIDField(default=uuid.UUID('0d48a506-2872-4398-b391-d9f4cdfff531')),
        ),
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 4, 22, 23, 41, 677714, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='token',
            name='token_body',
            field=models.UUIDField(default=uuid.UUID('379620a3-6b4e-4213-aab2-76fb5ade2d25')),
        ),
    ]

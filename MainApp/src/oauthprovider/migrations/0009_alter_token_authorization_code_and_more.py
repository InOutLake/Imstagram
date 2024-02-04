# Generated by Django 5.0.1 on 2024-02-01 05:25

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauthprovider', '0008_alter_token_authorization_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='authorization_code',
            field=models.UUIDField(default=uuid.UUID('146933ce-45e1-449e-ad83-4ba6070507c6')),
        ),
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 1, 18, 25, 48, 105470, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='token',
            name='token_body',
            field=models.UUIDField(default=uuid.UUID('89106101-211d-49ec-9b46-378646cc5da4')),
        ),
    ]

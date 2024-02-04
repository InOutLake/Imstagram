# Generated by Django 5.0.1 on 2024-01-31 15:09

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauthprovider', '0005_alter_token_authorization_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='authorization_code',
            field=models.UUIDField(default=uuid.UUID('d201b701-ccbb-4634-ba47-2b9f1e388381')),
        ),
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 1, 4, 9, 51, 813991, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='token',
            name='token_body',
            field=models.UUIDField(default=uuid.UUID('09a12a8a-6d25-4ce4-9657-04499601c6e9')),
        ),
    ]
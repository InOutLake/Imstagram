from collections.abc import Collection
from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import uuid

class Scope(models.Model):
    scope_name = models.CharField(primary_key=True, max_length=16)
    scope_info = models.TextField(null=False, max_length=256)

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_secret = models.UUIDField(unique=True, default=uuid.uuid4())

class Token(models.Model):
    token_id = models.AutoField(primary_key=True)
    token_body = models.UUIDField(null=False, default=uuid.uuid4())
    authorization_code = models.UUIDField(null=True, default=uuid.uuid4())
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE, null=False)
    expires_at = models.DateTimeField(null=False, auto_now=False, auto_now_add=False, 
                                      default=timezone.make_aware(datetime.now() + timedelta(hours=6)))
    authorization_code_expires_at = models.DateTimeField(null=False, auto_now=False, auto_now_add=False, 
                                      default=timezone.make_aware(datetime.now() + timedelta(minutes=5)))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    activated = models.BooleanField(default=False)

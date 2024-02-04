from django.contrib import admin
from .models import Scope, Client, Token

admin.site.register(Scope)
admin.site.register(Client)
admin.site.register(Token)
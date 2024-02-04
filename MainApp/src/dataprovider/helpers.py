from oauthprovider.models import Token
from Imstagram.models import Image
from django.utils import timezone
from rest_framework import serializers
from datetime import datetime
from functools import wraps
from django.http import HttpResponseForbidden, HttpResponseBadRequest


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_id', 'small_description', 'full_description', 'image', 'is_favorite')

class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Image
        fields = ['image']

def check_token_is_valid(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = args[1]
        if request.method == 'GET' and 'token' in request.GET:
            token_body = request.GET['token']
        elif request.method == 'POST' and 'token' in request.POST:
            token_body = request.POST['token']
        if not token_body:
            return HttpResponseBadRequest('Token is missing from the request.')
        token = get_token_by_token_body(token_body)
        if not token:
            return HttpResponseBadRequest('Token is expired or does not exist!')
        return view_func(*args, **kwargs)
    return _wrapped_view
    
def check_read_scope(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        token = get_token_by_token_body(args[1].GET['token'])
        if not token.scope.scope_name == 'Read':
            return HttpResponseForbidden('Insufficient permissions.')
    
        return view_func(*args, **kwargs)
    return _wrapped_view

def check_write_scope(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        token = get_token_by_token_body(args[1].POST['token'])
        if not token.scope.scope_name == 'Write':
            return HttpResponseForbidden('Insufficient permissions.')
    
        return view_func(*args, **kwargs)
    return _wrapped_view

def get_token_by_token_body(token_body):
    try:
        token = Token.objects.get(token_body=token_body)
        if token.expires_at < timezone.make_aware(datetime.now()):
            return None
        return Token.objects.get(token_body=token_body)
    except:
        return None
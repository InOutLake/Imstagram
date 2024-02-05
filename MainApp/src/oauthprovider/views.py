from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Client, Scope, Token
from django.views import View
from .forms import AuthorisationForm
from .helpers import get_client_by_id
from datetime import datetime, timedelta
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
import json

class Authorize(APIView):
    @swagger_auto_schema(
        operation_description='Authorization page that provides login form',
        responses={
            200: openapi.Response('Request data is valid', ),
            400: openapi.Response('Invalid input', ),
        },
        manual_parameters=[
            openapi.Parameter(
                name='client_id',
                in_=openapi.IN_QUERY,
                description='client_id registered in database',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='scope_name',
                in_=openapi.IN_QUERY,
                description='defines what access user will give to client. Could be Read, Write or All',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='redirect_uri',
                in_=openapi.IN_QUERY,
                description='defines uri where authorization code will be sent to',
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request):
        ''' 
        request should contain client_id, scope and redirect URL
        servier checks if id is valid
        present form with authorisation and grant info list 
        '''
        client_id = request.GET['client_id']
        scope_name = request.GET['scope_name']
        client = get_client_by_id(client_id)
        if client:
            context = {'scope_info': Scope.objects.get(scope_name=scope_name).scope_info,
                        'form': AuthorisationForm(request.GET)}
            return render(request, "authorize.html", context)
        else:
            return HttpResponseBadRequest("Invalid request!")

    @swagger_auto_schema(
        operation_description = 'if authorisation succeded, server creates authorisation code and \
                                redirects client to the redirect_uri/cb?code=\{authorization_code\}',
        responses={
            200: openapi.Response('Request data is valid, returns user to the redirect_uri/cb?code=\{authorization_code\}', example={'code': 'some_uuid'}),
            400: openapi.Response('Invalid input', ),
        },
        manual_parameters=[
            openapi.Parameter(
                name='client_id',
                in_=openapi.IN_QUERY,
                description='client_id registered in database',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='scope_name',
                in_=openapi.IN_QUERY,
                description='defines what access user will give to client. Could be Read, Write or All',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='redirect_uri',
                in_=openapi.IN_QUERY,
                description='defines uri where authorization code will be sent to',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='login',
                in_=openapi.IN_QUERY,
                description='user login',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='password',
                in_=openapi.IN_QUERY,
                description='user password',
                type=openapi.TYPE_STRING,
            )

        ]
    )
    def post(self, request):
        ''' 
        if authorisation succeded, server creates authorisation code and
        redirects client to the redirect URL
        '''
        form = AuthorisationForm(request.POST)
        if not form.is_valid():
            return render(request, 'authorize.html', {'form': form } )
        login = form.cleaned_data['login']
        password = form.cleaned_data['password']
        user = authenticate(username=login, password=password)
        if user and user.is_authenticated:
            scope = Scope.objects.get(scope_name=request.GET['scope_name'])
            client = Client.objects.get(client_id=request.GET['client_id'])
            token = Token.objects.create(user=user, scope=scope, client=client)
            authorization_code = token.authorization_code
            redirect_uri_base = request.GET['redirect_uri']
            redirect_uri = f'{redirect_uri_base}?code={authorization_code}'
            return HttpResponseRedirect(redirect_uri)
        else: 
            messages.error(request, "Authentication failed.")
            return render(request, 'authorize.html', {'form': form} )

class TokenView(APIView):
    @swagger_auto_schema(
        operation_description = 'verifies authorization_code and client_secret, returns grant token',
        responses={
            200: openapi.Response('Request data is valid, returns token', example={'token': 'some_uuid'}),
            400: openapi.Response('Invalid input', ),
        },
        manual_parameters=[
            openapi.Parameter(
                name='client_id',
                in_=openapi.IN_QUERY,
                description='client_id registered in database',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='client_secret',
                in_=openapi.IN_QUERY,
                description='client_secret registered in database',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='scope_name',
                in_=openapi.IN_QUERY,
                description='defines what access user will give to client. Could be Read, Write or All',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='redirect_uri',
                in_=openapi.IN_QUERY,
                description='defines uri where token will be sent to',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='code',
                in_=openapi.IN_QUERY,
                description='authorization_code that was sent by the server previously',
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def post(self, request):
        '''
        Verifies authorisation code, client_id, client_secret and grants an Token
        '''
        try:
            data = json.loads(request.body)
            client_id = int(data['client_id'])
            client_secret = data['client_secret']
            scope_name = data['scope_name']
            redirect_uri = data['redirect_uri']
            authorization_code = data['code']
            scope = Scope.objects.get(scope_name=scope_name)
            token = Token.objects.get(authorization_code=authorization_code)

            if not token:
                return HttpResponseBadRequest("Token expired or does not exist")

            if not token.client.client_id == client_id:
                return HttpResponseBadRequest("Wrong client")

            if not str(token.client.client_secret) == client_secret:
                return HttpResponseBadRequest("Wrong client secret")

            if not token.scope == scope:
                return HttpResponseBadRequest("Wrong scope")
            
            if not token.activated and token.authorization_code_expires_at < timezone.make_aware(datetime.now()):
                return HttpResponseBadRequest("Token expired")

            token.activated = True
            data = {
                'token': str(token.token_body)
            }
            return JsonResponse(data=data)
        except:
            return HttpResponseBadRequest("Invalid request!")


class RegisterApp(View):
    def get(self, request):
        return render(...)
    
    def post(self, request):
        ...
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest, FileResponse
from Imstagram.models import Image
from oauthprovider.models import Token, Scope
from .helpers import get_token_by_token_body, ImageModelSerializer, check_read_scope, check_write_scope, check_token_is_valid
from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import *
import zipfile, io
from rest_framework.generics import ListAPIView
import json

class ProvideImagesInfo(ListAPIView):
    serializer_class = ImageModelSerializer
    permission_classes = [HasValidToken, HasReadPermission]

    def get_queryset(self):
        """
        Retrieve all image info in QuerySet<ImageModel>.
        """
        token_body = self.request.GET.get('token')
        token = get_token_by_token_body(token_body)
        return Image.objects.filter(image_owner=token.user)

class ProvideImages(APIView):
    permission_classes = [HasValidToken, HasReadPermission]
    
    @swagger_auto_schema(
        operation_description='Retrieve all images owned by the authenticated user as a ZIP file',
        responses={
            200: openapi.Response('A ZIP file containing all images owned by the user', ),
            400: openapi.Response('Invalid input', ),
        },
        manual_parameters=[
            openapi.Parameter(
                name='token',
                in_=openapi.IN_QUERY,
                description='The token identifying the user',
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request):
        """
        Retrieve all images owned by the authenticated user as a ZIP file.
        """
        token_body = request.GET['token']
        token = get_token_by_token_body(token_body)
        user = token.user
        images = Image.objects.filter(image_owner=user)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for image in images:
                image_path = image.image.path
                if default_storage.exists(image_path):
                    with default_storage.open(image_path, 'rb') as img_file:
                        zip_file.writestr(image.image.name.removeprefix(f'images/{user.get_username()}/'), img_file.read())
        zip_buffer.seek(0)
        return FileResponse(zip_buffer)

class SaveImageInstance(APIView):
    serializer_class = ImageModelSerializer
    permission_classes = [HasValidToken, HasWritePermission]

    @swagger_auto_schema(
        operation_description='Save an ImageModel including the image file',
        responses={
            201: openapi.Response('ImageModel instance has bee successfully created', ),
            400: openapi.Response('Invalid input', ),
        },
        manual_parameters=[
            openapi.Parameter(
                name='token',
                in_=openapi.IN_QUERY,
                description='The token identifying the user',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='image_instance_info',
                in_=openapi.IN_QUERY,
                description="json string containing 'small_description' and 'full_description' fields ",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name='image',
                in_=openapi.IN_QUERY,
                description='image file of image/jpeg type',
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def post(self, request):
        try:
            image_instance_info_str = request.POST['image_instance_info']
            image_instance_info = json.loads(image_instance_info_str)
        except ValueError:
            return Response({'error': 'Invalid JSON'}, status=400)
        
        token = get_token_by_token_body(request.POST['token'])
        if 'image' not in request.FILES:
            return Response({'error': 'No image file was provided'}, status=400)

        image_file = request.FILES['image']
        user = token.user
        image_instance = Image(image=image_file, image_owner=user, **image_instance_info)
        image_instance.save()

        return Response({'message': 'Image saved successfully'}, status=201)

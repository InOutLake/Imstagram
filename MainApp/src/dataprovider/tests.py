from django.test import TestCase, Client as TestClient
from oauthprovider.models import Client, Scope, Token
from Imstagram.models import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from MainApp.settings import MEDIA_ROOT, BASE_DIR
from django.test import RequestFactory
from .views import SaveImageInstance
import uuid, tempfile, zipfile, re, os, shutil, json, io

class GetViewsTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.test_client_secret='c7359a4a-fa96-42ff-84aa-fe61bc8a3f24'
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.client_obj = Client.objects.create(client_secret = self.test_client_secret)
        self.scope = Scope.objects.create(scope_name='Read', scope_info='test_info')
        self.authorization_code =  uuid.uuid4()
        self.test_token = Token.objects.create(user=self.user, scope=self.scope, authorization_code=self.authorization_code,
                                                client=self.client_obj)
        self.Image1 = Image.objects.create(
            image_owner=self.user,
            image=SimpleUploadedFile(
                name='test.jpg',
                content=b'test_content',
                content_type='image/jpeg'
            )
        )
        self.Image2 = Image.objects.create(
            image_owner=self.user,
            image=SimpleUploadedFile(
                name='test.jpg',
                content=b'test_content',
                content_type='image/jpeg'
            )
        )

    def test_provide_images_info(self):
        endpoint = '/dataprovider/provide_images_info/'
        headers = {'token': self.test_token.token_body}
        response = self.client.get(endpoint, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_provide_images(self):
        endpoint = '/dataprovider/provide_images/'
        headers = {'token': self.test_token.token_body}
        response = self.client.get(endpoint, headers=headers)
        self.assertEqual(response.status_code, 200)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in response.streaming_content:
                temp_file.write(chunk)
            temp_file.flush()
            with zipfile.ZipFile(temp_file.name, 'r') as zip_ref:
                zip_ref.extractall(BASE_DIR/'dataprovider/test_unzipped_images')
        actual_images_names = [self.Image1.image.name.removeprefix('images/test_user/'),
                               self.Image2.image.name.removeprefix('images/test_user/')]
        actual_images_names.sort()
        unzipped_images_names = os.listdir(BASE_DIR / 'dataprovider/test_unzipped_images/')
        unzipped_images_names.sort()
        self.assertEqual(unzipped_images_names, actual_images_names)
        
    @classmethod
    def tearDownClass(cls):
        for file in os.listdir(MEDIA_ROOT / 'images/test_user'):
            if re.match(r'test[^\.]+\.jpg', file):
                os.remove(MEDIA_ROOT / f'images/test_user/{file}')
        shutil.rmtree(BASE_DIR / 'dataprovider/test_unzipped_images')
        return super().tearDownClass()
    

class SaveImageInstanceTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.client_obj = Client.objects.create()
        self.test_user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.test_scope = Scope.objects.create(scope_name='Write', scope_info='test_description')
        self.test_token = Token.objects.create(user=self.test_user, scope=self.test_scope,
                                               client=self.client_obj)
        self.image_instance_info = {
            'small_description': 'test_small_description',
            'full_description': 'test_full_description'
        }
        self.image_instance_info_str = json.dumps(self.image_instance_info)
        self.image_file = SimpleUploadedFile('test_image.jpg', b'test_content', content_type='image/jpeg')
        self.image_file.seek(0)

    def test_save_image_instance(self):
        endpoint = '/dataprovider/save_image_instance/'
        data = {
            'image_instance_info': self.image_instance_info_str,
            'image': self.image_file
        }
        headers = {'token': self.test_token.token_body,}
        response = self.client.post(endpoint, data=data, headers=headers)

        self.assertEqual(response.status_code, 201)

        image_instance = Image.objects.first()
        self.assertIsNotNone(image_instance)

        self.assertEqual(image_instance.small_description, self.image_instance_info['small_description'])
        self.assertEqual(image_instance.full_description, self.image_instance_info['full_description'])

        self.assertIsNotNone(image_instance.image)
        self.assertIsNotNone(re.match(r'^.*\/test_image.*\.jpg$', image_instance.image.name))
        os.remove(MEDIA_ROOT/'images/test_user/test_image.jpg')

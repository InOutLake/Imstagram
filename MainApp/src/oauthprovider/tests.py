from django.test import TestCase, Client as TestClient
from django.contrib.auth import get_user_model
from .models import Client, Scope, Token
from datetime import datetime, timedelta
import uuid, json

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.test_client_secret='c7359a4a-fa96-42ff-84aa-fe61bc8a3f24'
        self.user = get_user_model().objects.create_user(username='test_user', password='test_password')
        self.client_obj = Client.objects.create(client_secret = self.test_client_secret)
        self.scope = Scope.objects.create(scope_name='Read', scope_info='test_info')
        self.redirect_uri = "http://localhost:8000/oauth/token/"
        self.authorization_code =  uuid.uuid4()
        self.test_token = Token.objects.create(user=self.user, scope=self.scope, authorization_code=self.authorization_code,
                                                client=self.client_obj)

    def test_Authorize_get(self):
        endpoint = "/oauth/authorize/"
        data = {
            'client_id': self.client_obj.client_id,
            'scope_name': self.scope.scope_name
        }
        response = self.client.get(endpoint, data=data)
        self.assertEqual(response.status_code, 200)

    def test_Token_post(self):
        endpoint = '/oauth/token/'
        data = {
            'client_id': self.client_obj.client_id,
            'client_secret': str(self.test_client_secret),
            'scope_name': self.scope.scope_name,
            'redirect_uri': self.redirect_uri,
            'code': str(self.authorization_code),
        }
        json_data = json.dumps(data)
        encoded_data = json_data.encode('utf-8')
        response = self.client.post(endpoint, data=encoded_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
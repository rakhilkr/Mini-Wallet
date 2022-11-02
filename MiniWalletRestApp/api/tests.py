from django.urls import reverse
from django.contrib.auth.hashers import make_password
import os
from django.utils import timezone
from rest_framework.authtoken.models import Token
from datetime import datetime
from urllib.parse import urlencode
from django.test import (
    Client,
    TestCase,
)
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from django.contrib.auth import get_user_model
from datetime import datetime

from .models import Wallet



class BaseTestCase(TestCase):
    """Core Test."""
    username = "ea0212d3-abd6-406f-8c67-868e814a2436"
    user_email = "Test@gmail.com"
    user_password = 'Test@1234'
    User = get_user_model()

    def setUp(self):
        """Setup."""

        self.user = self.User(
            username=self.username,
            email="Test@gmail.com",
            first_name="Test",
            last_name="User",
            is_active=True,
            is_superuser=True,
        )
        self.user.set_password('Test@1234')
        self.user.save()

        self.token = Token.objects.create(user=self.user)
        self.token.save()

        # Every test needs a client.
        self.client =  Client()

        # Login as user
        logged_in = self.client.login(username=self.username)
        self.assertTrue(logged_in)
        client = APIClient()
        self.token_data = 'Token ' + self.token.key
        client.credentials(Authorization=self.token_data)
        client.force_authenticate(user=self.user)

        wallet = Wallet()
        wallet.owned_by = self.user
        wallet.status = 'DISABLED'
        wallet.enabled_at = datetime.now()
        wallet.balance = 100
        wallet.save()

    def tearDown(self):
        """Teardown."""
        pass

    def _assert_success_code(self, response):
        content = response.json()
        self.assertEqual(response.status, 'success')
        self.assertIn('data', content)
        data = content.get('data')
        if type(data) is list and len(data) > 0:
            data = data[0]
        return (content, data)


class APITestCase(BaseTestCase):
    """Test for Initializing Wallet."""

    def test_001_wallet_initialize_api_url(self):
        """Wallet_initialize_api_url."""

        # Success Case
        response = self.client.post('http://127.0.0.1:8000/api/v1/init', data={"customer_xid":self.user.username})
        self.assertEqual(response.status_code, 200)

        # Error Case
        response = self.client.get('http://127.0.0.1:8000/api/v1/init')
        self.assertEqual(response.status_code, 405)

    def test_002_wallet_api_url(self):
        """Wallet__api_url."""

        response = self.client.get('http://127.0.0.1:8000/api/v1/wallet', headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, 200)

    def test_003_enable_wallet_api_url(self):
        """Wallet_enable_api_url."""

        response = self.client.post('http://127.0.0.1:8000/api/v1/wallet', headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, 200)



    def test_003_disable_wallet_api_url(self):
        """Wallet_disable_api_url."""

        response = self.client.patch('http://127.0.0.1:8000/api/v1/wallet', headers={'Authorization': 'Token ' + self.token.key})
        self.assertEqual(response.status_code, 200)
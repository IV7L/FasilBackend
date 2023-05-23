from django.contrib.auth.backends import ModelBackend
from account.models import Account
#Web3
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
# Basic
from django.conf import settings
#Signnature verify imports
from web3 import Web3, HTTPProvider
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/3f8783d83dc14864a098005310eb73a5"))
from rest_framework.authentication import TokenAuthentication

class EthereumAuthenticationBackend(TokenAuthentication):
    def authenticate(self, request, ethereum_address=None, password=None, **kwargs):
        try:
            user = Account.objects.get(ethereum_address=ethereum_address)
            return user if user.check_password(password) else None
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None

    def create_user(self, ethereum_address):
        user = Account.objects.create_user(
            username=ethereum_address,
            password=None,
        )
        return user
    def authenticate_header(self, request):
        # Return custom authenticate header value for Ethereum authentication
        return 'Ethereum'
    
class BasicAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if not username or not password:
            return None

        user_model = get_user_model()

        if username == settings.BASIC_AUTH_USERNAME and password == settings.BASIC_AUTH_PASSWORD:
            try:
                user = user_model.objects.get(username=username)
                return user
            except user_model.DoesNotExist:
                return None

        return None
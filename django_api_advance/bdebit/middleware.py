from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.conf import settings

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the response contains BVN debit details
        if hasattr(response, 'data') and 'bvn' in response.data:
            # Generate a random 16-byte key
            key = get_random_bytes(16)
            aes_cipher = AESCipher(key)

            # Encrypt BVN debit details in the response
            iv, ct = aes_cipher.encrypt(response.data['bvn'])
            response.data['encrypted_bvn'] = {'iv': iv, 'encrypted_data': ct}

            # Remove original BVN debit details from the response
            del response.data['bvn']

        return response

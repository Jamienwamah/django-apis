from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.conf import settings

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

       # Encrypt response data
        key = settings.SECRET_KEY.encode('utf-8')  # Get the secret key from Django settings
        aes_cipher = AES.new(key, AES.MODE_CBC)
        encrypted_data = aes_cipher.encrypt(pad(response.content, AES.block_size))
        response.content = b64encode(aes_cipher.iv + encrypted_data)


        return response

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.conf import settings

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Intercept request data before it's processed by the view
        if request.method == 'POST':
            # Encrypt sensitive information before storing it in the database
            aes_cipher = AESCipher(settings.SECRET_KEY)
            request.data['description_iv'], request.data['description'] = aes_cipher.encrypt(request.data['description'])

        response = self.get_response(request)

        # Intercept response data before it's sent to the client
        if hasattr(response, 'data') and 'description' in response.data:
            # Decrypt sensitive information before sending it to the client
            aes_cipher = AESCipher(settings.SECRET_KEY)
            response.data['description'] = aes_cipher.decrypt(response.data['description_iv'], response.data['description'])

        return response

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt(self, iv, data):
        cipher = AES.new(self.key, AES.MODE_CBC, b64decode(iv))
        pt = unpad(cipher.decrypt(b64decode(data)), AES.block_size)
        return pt.decode('utf-8')

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.conf import settings

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(response, 'data'):
            if 'encrypted_reset_token_iv' in response.data and 'encrypted_reset_token' in response.data:
                # Decrypt the reset password token in the response
                key = settings.SECRET_KEY.encode('utf-8')
                aes_cipher = AESCipher(key)
                decrypted_reset_token = aes_cipher.decrypt(response.data['encrypted_reset_token_iv'], response.data['encrypted_reset_token'])
                response.data['reset_token'] = decrypted_reset_token

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

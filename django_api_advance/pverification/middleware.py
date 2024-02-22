from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import jwt
from django.conf import settings

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path == '/verify_phone_number/':
            if request.method == 'POST':
                # Decrypt encrypted_verification_code received in the request
                encrypted_verification_code = request.data.get('encrypted_verification_code')
                decrypted_verification_code = self.decrypt_verification_code(encrypted_verification_code)
                request.data['verification_code'] = decrypted_verification_code

        return response

    @staticmethod
    def encrypt_verification_code(verification_code):
        aes_cipher = AES.new(settings.SECRET_KEY[:32], AES.MODE_CBC)
        encrypted_code = aes_cipher.encrypt(pad(verification_code.encode(), AES.block_size))
        return b64encode(encrypted_code).decode()

    def decrypt_verification_code(self, encrypted_code):
        aes_cipher = AES.new(settings.SECRET_KEY[:32], AES.MODE_CBC)
        decrypted_code = unpad(aes_cipher.decrypt(b64decode(encrypted_code)), AES.block_size)
        return decrypted_code.decode()

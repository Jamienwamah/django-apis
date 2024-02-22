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
        
        if request.path == '/register/':
            # Encrypt OTP code before saving it to the database
            if request.method == 'POST':
                otp_code = response.data.get('otp_code')
                encrypted_otp = self.encrypt_otp(otp_code)
                response.data['encrypted_otp'] = encrypted_otp

        if request.path == '/verify/otp/':
            # Decrypt OTP code received in the request
            if request.method == 'POST':
                jwt_token = request.data.get('jwt_token')
                decrypted_otp = self.decrypt_otp(jwt_token)
                request.data['otp_code'] = decrypted_otp

        return response

    def encrypt_otp(self, otp_code):
        aes_key = settings.SECRET_KEY[:32]
        aes_cipher = AES.new(aes_key, AES.MODE_CBC)
        encrypted_otp = aes_cipher.encrypt(pad(str(otp_code).encode(), AES.block_size))
        return b64encode(encrypted_otp).decode()

    def decrypt_otp(self, jwt_token):
        decrypted_jwt = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        encrypted_otp = b64decode(decrypted_jwt['otp'])
        aes_key = settings.SECRET_KEY[:32]
        aes_cipher = AES.new(aes_key, AES.MODE_CBC)
        decrypted_otp = unpad(aes_cipher.decrypt(encrypted_otp), AES.block_size)
        return decrypted_otp.decode()

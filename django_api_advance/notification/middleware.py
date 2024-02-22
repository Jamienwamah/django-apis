from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import jwt
from django.conf import settings

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            # Intercept request data before it's processed by the view
            data = request.data

            # Generate AES key
            aes_key = get_random_bytes(16)
            aes_cipher = AESCipher(aes_key)

            # Encrypt notification content
            iv, encrypted_content = aes_cipher.encrypt(data['content'])
            data['encrypted_content'] = encrypted_content.hex()
            data['iv'] = iv.hex()

            # Generate and encode JWT token
            token = jwt.encode({'user_id': request.user.id}, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
            data['token'] = token

            # Update request data
            request.data = data

        response = self.get_response(request)

        if hasattr(response, 'data') and 'content' in response.data:
            # Intercept response data before it's sent to the client
            data = response.data

            # Decrypt notification content
            aes_key = response.data['aes_key']
            iv = bytes.fromhex(response.data['iv'])
            encrypted_content = bytes.fromhex(response.data['encrypted_content'])
            aes_cipher = AESCipher(aes_key)
            decrypted_content = aes_cipher.decrypt(iv, encrypted_content)
            data['content'] = decrypted_content

            # Update response data
            response.data = data

        return response

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = cipher.iv
        ct = ct_bytes
        return iv, ct

    def decrypt(self, iv, data):
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(data), AES.block_size)
        return pt.decode('utf-8')

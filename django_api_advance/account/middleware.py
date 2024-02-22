from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

class AESCipherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        if response.status_code == 200 and 'encrypted_data' in response.data:
            # Encrypt the response data if it contains 'encrypted_data'
            encrypted_data = response.data['encrypted_data']
            key = get_random_bytes(16)
            aes_cipher = AESCipher(key)
            encrypted_content = aes_cipher.encrypt(encrypted_data)
            response.data['encrypted_data'] = encrypted_content
        return response

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        return {'iv': iv, 'encrypted_data': ct}

    def decrypt(self, iv, data):
        cipher = AES.new(self.key, AES.MODE_CBC, b64decode(iv))
        pt = unpad(cipher.decrypt(b64decode(data)), AES.block_size)
        return pt.decode('utf-8')

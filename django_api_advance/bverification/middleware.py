from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import os

class EncryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request data
        if request.method == 'POST' and request.path == '/api/bvn_verification/':  # Assuming the VN verification endpoint is '/api/bvn_verification/'
            bvn = request.data.get('bvn')
            key = self.generate_aes_key()

            encrypted_bvn = self.encrypt_bvn(bvn, key)
            request.data['encrypted_bvn'] = encrypted_bvn

        response = self.get_response(request)

        # Process response data
        if request.method == 'GET' and request.path == '/api/bvn_verification/':  # Assuming the VN verification endpoint is '/api/bvn_verification/'
            encrypted_bvn = response.data.get('encrypted_bvn')
            key = self.get_aes_key()  # Assuming the key is stored in the user's session or retrieved from a secure location

            decrypted_bvn = self.decrypt_bvn(encrypted_bvn, key)
            response.data['decrypted_bvn'] = decrypted_bvn

        return response

    def encrypt_bvn(self, bvn, key):
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(bvn.encode(), AES.block_size))
        encrypted_bvn = b64encode(ct_bytes).decode()
        return encrypted_bvn

    def decrypt_bvn(self, encrypted_bvn, key):
        cipher = AES.new(key, AES.MODE_CBC)
        pt = unpad(cipher.decrypt(b64decode(encrypted_bvn)), AES.block_size)
        decrypted_bvn = pt.decode('utf-8')
        return decrypted_bvn

    @staticmethod
    def generate_aes_key():
        # Generate a random 16-byte AES key
        key = os.urandom(16)
        return key

    def get_aes_key(self):
        # Retrieve the AES key from the user's session or from a secure location
        # For demonstration purposes, we're generating a new key here
        return self.generate_aes_key()

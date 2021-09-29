import rsa
from rsa import PublicKey, PrivateKey

class encryptor:
    def __init__(self):
        pass

    def set_encryption(self, num_of_char):
        public_key, private_key = rsa.newkeys(num_of_char)
        public_key_pkcs1_pem = public_key.save_pkcs1()
        private_key_pkcs1_pem = private_key.save_pkcs1()
        with open('public_key.pem', 'wb') as f:
            f.write(public_key_pkcs1_pem)
        with open('private_key.pem', 'wb') as f:
            f.write(private_key_pkcs1_pem)
        return public_key_pkcs1_pem.decode(), private_key_pkcs1_pem.decode()
    def encrypt(self, msg):
        public_key_file = open('public_key.pem', 'rb').read()
        public_key = PublicKey.load_pkcs1(public_key_file, format='PEM')
        encrypted_msg = rsa.encrypt(msg.encode(), public_key)
        return encrypted_msg
    
    def decrypt(self, msg):
        private_key_file = open('private_key.pem', 'rb').read()
        private_key = PrivateKey.load_pkcs1(private_key_file, format='PEM')
        decrypted_msg = rsa.decrypt(msg, private_key).decode()
        return decrypted_msg


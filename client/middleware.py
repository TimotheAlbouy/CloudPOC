from client.crypto import ope_encrypt, he_encrypt, ope_decrypt, he_decrypt
from client.constants import HE_PUBLIC_KEY
from server.middleware import ServerMiddleware


class ClientMiddleware:

    def __init__(self):
        self.server = ServerMiddleware(HE_PUBLIC_KEY)

    def create_variable(self, name, value):
        ope_cipher = ope_encrypt(value)
        he_cipher = he_encrypt(value)
        self.server.create_encrypted_variable(name, ope_cipher, he_cipher)

    def get_variable(self, name):
        encrypted_variable = self.server.get_encrypted_variable(name)
        if encrypted_variable is None:
            return None
        value = ope_decrypt(encrypted_variable[1])
        variable = (name, value)
        return variable

    def update_variable(self, name, value):
        ope_cipher = ope_encrypt(value)
        he_cipher = he_encrypt(value)
        self.server.update_ope_cipher(name, ope_cipher)
        self.server.update_he_cipher(name, he_cipher)

    def delete_variable(self, name):
        self.server.delete_encrypted_variable(name)

    def compare_variables(self, name1, name2):
        return self.server.compare_ciphers(name1, name2)

    def add_variables(self, source1, source2, destination):
        he_cipher = self.server.add_ciphers(source1, source2)
        value = he_decrypt(he_cipher)
        ope_cipher = ope_encrypt(value)
        self.server.update_ope_cipher(destination, ope_cipher)
        self.server.update_he_cipher(destination, he_cipher)

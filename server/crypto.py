from phe import EncryptedNumber


def add_ciphers(public_key, cipher1, cipher2):
    n1 = EncryptedNumber(public_key, cipher1)
    n2 = EncryptedNumber(public_key, cipher2)
    result = n1 + n2
    return result.ciphertext()

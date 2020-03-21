from client.constants import OPE_SECRET_KEY, HE_PUBLIC_KEY, HE_PRIVATE_KEY


def ope_encrypt(value):
    return OPE_SECRET_KEY.encrypt(value)


def he_encrypt(value):
    return HE_PUBLIC_KEY.raw_encrypt(value)


def ope_decrypt(cipher):
    return OPE_SECRET_KEY.decrypt(cipher)


def he_decrypt(cipher):
    return HE_PRIVATE_KEY.raw_decrypt(cipher)

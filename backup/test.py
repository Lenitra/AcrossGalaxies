

# print(secret_key)


from cryptography.fernet import Fernet

secret_key = b'gZTtOPorjsy8tdTFeLWXKWqG9EcX1Ifd1oiaFDXgFFg='



def encode(message: str):
    key = secret_key
    message = bytes(message, "utf-8")
    return Fernet(key).encrypt(message)


def decode(token: bytes):
    key = secret_key
    return (Fernet(key).decrypt(token)).decode("utf-8")

a = "un cheval blanc"
a = encode(a)
print(decode(a), "     ", decode(a))
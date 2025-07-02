from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import json


key = RSA.generate(2048)
public_key = key.publickey()
with open('public.pem', 'wb') as pem:
    pem.write(public_key.export_key())
private_key = key


def encrypt(message: str, pub_key: RSA.RsaKey):
    cipher = PKCS1_OAEP.new(pub_key)
    ciphertext = cipher.encrypt(message.encode())
    return base64.b64encode(ciphertext)

def decrypt(ciphertext_b64: str, priv_key: RSA.RsaKey):
    cipher = PKCS1_OAEP.new(priv_key)
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()

if __name__ == "__main__":
    message = json.dumps('ji')
    ciphertext1 = encrypt(message, public_key)
    decrypted1 = json.loads(decrypt(ciphertext1, private_key))
    print(decrypted1, type(decrypted1))

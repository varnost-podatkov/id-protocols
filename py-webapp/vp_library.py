# Import necessary modules
import os
import secrets
import string

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def generate_response_hmac_256(key: bytes, challenge: str) -> str:
    mac_algorithm = hmac.HMAC(key, hashes.SHA256())
    mac_algorithm.update(challenge.encode("utf8"))
    mac_tag = mac_algorithm.finalize()

    number = (int.from_bytes(mac_tag[0:4], byteorder="big") & 0x7FFFFFFF) % 1000000
    return "{:06d}".format(number)


def generate_challenge(digits: int) -> string:
    return ''.join(secrets.choice(string.digits) for _ in range(digits))


def hash_password(password: str) -> (bytes, bytes):
    salt = os.urandom(16)

    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1, )
    hashed = kdf.derive(password.encode("utf8"))

    return salt, hashed


def verify_password(attempt: str, salt: bytes, hashed: bytes) -> bool:
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1, )
    try:
        kdf.verify(attempt.encode("utf8"), hashed)
        return True
    except InvalidKey:
        return False

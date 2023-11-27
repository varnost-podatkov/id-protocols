# Import necessary modules
import os
import string

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def generate_response_hmac_256(key: bytes, challenge: str) -> str:
    """Izračuna odziv za podan poziv"""

    # Pri implementaciji si pomagajate z Javansko različico:
    #  String generateResponseHMAC256(byte[] key, String challenge)
    mac_algorithm = hmac.HMAC(key, hashes.SHA256())
    mac_algorithm.update(challenge.encode("utf8"))
    mac_tag = mac_algorithm.finalize()

    number = (int.from_bytes(mac_tag[0:4], byteorder="big") & 0x7FFFFFFF) % 1000000
    return "{:06d}".format(number)


def generate_challenge() -> string:
    """Ustvari naključno 6-mestno številko"""
    rnd = os.urandom(4)
    number = int.from_bytes(rnd, byteorder="big")
    number = number & 0x7FFFFFFF  # nastavi MSB na 0 (da bo pozitivno)
    number = number % 1000000  # ostanek pri deljenju z 10^6 da 6-mestno število
    # vrnemo 6 mestni niz: če je število manj-mestno, ga podložimo z ničlami
    return "{:06d}".format(number)


def hash_password(password: str) -> (bytes, bytes):
    """Iz podanega gesla izračuna zgoščeno vrednost s funkcijo scrypt.

    Vrne par (sol, zgoščena) vrednost"""
    salt = os.urandom(16)

    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    hashed = kdf.derive(password.encode("utf8"))

    return salt, hashed


def verify_password(attempt: str, salt: bytes, hashed: bytes) -> bool:
    """Vzame niz poskus, bajte sol in bajte, ki predstavljajo zgoščeno vrednost
    pravega gesla in vrne True ntk. je poskus gesla pravilen. Sicer vrne False."""
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    try:
        kdf.verify(attempt.encode("utf8"), hashed)
        return True
    except InvalidKey:
        return False

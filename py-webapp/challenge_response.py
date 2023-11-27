# Import necessary modules
import secrets
import string

from cryptography.hazmat.primitives import hashes, hmac


def generate_response_hmac_256(key: bytes, challenge: str) -> str:
    mac_algorithm = hmac.HMAC(key, hashes.SHA256())
    mac_algorithm.update(challenge.encode("utf8"))
    mac_tag = mac_algorithm.finalize()

    number = (int.from_bytes(mac_tag[0:4], byteorder="big") & 0x7FFFFFFF) % 1000000
    return "{:06d}".format(number)


def generate_challenge(digits: int) -> string:
    return ''.join(secrets.choice(string.digits) for _ in range(digits))

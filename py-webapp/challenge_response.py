# Import necessary modules

from cryptography.hazmat.primitives import hashes, hmac


def generate_response_hmac_256(key: object, challenge: object) -> object:
    mac_algorithm = hmac.HMAC(key, hashes.SHA256())
    mac_algorithm.update(challenge.encode("utf8"))
    mac_tag = mac_algorithm.finalize()

    number = (int.from_bytes(mac_tag[0:4], byteorder="big") & 0x7FFFFFFF) % 1000000
    return "{:06d}".format(number)


key = "581f22628ce7b73da43abfceb41c94a5"
print(generate_response_hmac_256(bytes.fromhex(key), "challenge"))

# Import necessary modules
import time

from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.twofactor.hotp import HOTP

# Run the application if the script is executed
if __name__ == '__main__':
    totp = HOTP(bytes.fromhex("581f22628ce7b73da43abfceb41c94a5"), 6, SHA1())
    for i in range(5):
        print(totp.generate(i).decode("utf8"))

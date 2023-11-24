# Import necessary modules
import time

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.twofactor.totp import TOTP

# Run the application if the script is executed
if __name__ == '__main__':
    totp = TOTP(bytes.fromhex("581f22628ce7b73da43abfceb41c94a5"), 6, SHA256(), 30)
    while True:
        t = int(time.time())
        print(totp.generate(t).decode("utf8"))
        time.sleep(1)

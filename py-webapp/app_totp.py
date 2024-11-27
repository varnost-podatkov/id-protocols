import time

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from flask import Flask, request

app = Flask(__name__)

# Uporabniki
# - Vsak bi moral imeti drug kljuc, a namenoma poenostavljamo
users = {
    'ana': "581f22628ce7b73da43abfceb41c94a5",
    'bor': "581f22628ce7b73da43abfceb41c94a5",
    'cene': "581f22628ce7b73da43abfceb41c94a5",
}


@app.route('/', methods=['GET'])
def login():
    return '''
        <!doctype html>
        <h1>TOTP Login</h1>
        <form action="/validate" method="post">
            Username: <input type="text" name="username"><br>
            OTP: <input type="text" name="otp"><br>
            <br>
            <input type="submit" value="Login">
        </form>
        <p>[ <a href="/">Log-in</a> ]
    '''


@app.route('/validate', methods=['POST'])
def validate_user_pass():
    # Get username and password from the form
    username = request.form['username']
    otp = request.form['otp']

    message = "Invalid username."
    if username in users:
        totp = TOTP(bytes.fromhex(users[username]), 6, SHA256(), 30)
        try:
            totp.verify(otp.encode("ascii"), int(time.time()))
            message = f"Welcome, {username}, OTP was correct."
        except InvalidToken:
            message = "Invalid OTP."

    return f'''
        <!doctype html>
        <h1>TOTP Login status</h1>
        <p>{message}
        <p>[ <a href="/">Log-in</a> ]
    '''


if __name__ == '__main__':
    app.run(debug=True)

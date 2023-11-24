# Import necessary modules
import os
import secrets
import string
import time

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from flask import Flask, request

app = Flask(__name__)

# poznano le aplikaciji
app_key = os.urandom(16)

# Uporabniki

users = {
    'ana': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "password": "vp",
        "challenge": None},
    'bor': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "password": "vp",
        "challenge": None},
    'cene': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "password": "vp",
        "challenge": None},
}


@app.route('/', methods=['GET'])
def login():
    return '''
        <form action="/validate-user-password" method="post">
            Username: <input type="text" name="username"><br>
            Username: <input type="password" name="password"><br>
            <br>
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/validate-user-password', methods=['POST'])
def validate_user_pass():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]["password"] == password:
        challenge = ''.join(secrets.choice(string.digits) for _ in range(6))
        users[username]["challenge"] = challenge


        # generate challenge
        # write it to DB


    if username in users:
        totp = TOTP(bytes.fromhex(users[username]), 6, SHA256(), 30)
        try:
            totp.verify(otp.encode("ascii"), int(time.time()))
            return f"Welcome, {username}, OTP was correct."
        except InvalidToken:
            return "Invalid OTP."
    return 'Invalid username.'


@app.route('/validate', methods=['POST'])
def validate_user_pass():
    # Get username and password from the form
    username = request.form['username']
    otp = request.form['otp']

    if username in users:
        totp = TOTP(bytes.fromhex(users[username]), 6, SHA256(), 30)
        try:
            totp.verify(otp.encode("ascii"), int(time.time()))
            return f"Welcome, {username}, OTP was correct."
        except InvalidToken:
            return "Invalid OTP."
    return 'Invalid username.'


# Run the application if the script is executed
if __name__ == '__main__':
    app.run(debug=True)

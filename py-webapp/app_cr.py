# Import necessary modules
import os
import secrets
import string

from cryptography.hazmat.primitives import constant_time
from flask import Flask, request

import challenge_response

app = Flask(__name__)

# poznano le aplikaciji
app_key = os.urandom(16)

# Uporabniki
# Vsak uporabnik ima isti ključ -- to je napačno
# Primer je poenostavljen zaradi demonstracije
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
        <form action="/validate-user" method="post">
            Username: <input type="text" name="username"><br>
            <br>
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/validate-user', methods=['POST'])
def validate_user_pass():
    username = request.form['username']

    assert username in users, "Invalid username."  # hitro preverjanje

    challenge = ''.join(secrets.choice(string.digits) for _ in range(6))
    users[username]["challenge"] = challenge

    return f'''
        <form action="/validate-response" method="post">
            Username: {username}<br><input type="hidden" name="username" value="{username}"><br>
            Password: <input type="password" name="password"><br>
            Challenge: <b>{challenge}</b><br>
            OTP: <input type="text" name="otp"><br>
            <br>
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/validate-response', methods=['POST'])
def validate_response():
    # Get username, password and OTP
    username = request.form['username']
    password = request.form['password']
    otp = request.form['otp']

    # Napake so zgolj v pomoč pri razhroščevanju
    # V produkciji ne povemo, kaj je razlog
    assert username in users, "Invalid username"
    assert users[username]["password"] == password, "Invalid password"
    assert len(otp) == 6, "Invalid OTP"

    # TODO Validate otp
    recomputed = challenge_response.generate_response_hmac_256(
        bytes.fromhex(users[username]["key"]),
        users[username]["challenge"])
    if not constant_time.bytes_eq(recomputed.encode("utf8"), otp.encode("utf8")):
        return "Invalid OTP"

    return f"Welcome, {username}, OTP was correct."


# Run the application if the script is executed
if __name__ == '__main__':
    app.run(debug=True)

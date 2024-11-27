from cryptography.hazmat.primitives import constant_time
from flask import Flask, request

import vp_library

app = Flask(__name__)

# Baza uporabnikov
# - Vsak bi moral imeti svoj kljuc, a namenoma poenostavljamo
users = {
    'ana': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "challenge": None},
    'bor': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "challenge": None},
    'cene': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "challenge": None},
}


@app.route('/', methods=['GET'])
def login():
    return '''
        <!doctype html>
        <h1>Challenge-Response: Login</h1>
        <form action="/validate-user" method="post">
            Username: <input type="text" name="username"><br>
            <br>
            <input type="submit" value="Login">
        </form>
        <p>[ <a href="/">Log-in</a> ]'''


@app.route('/validate-user', methods=['POST'])
def validate_user_pass():
    username = request.form['username']

    assert username in users, "Invalid username."  # hitro preverjanje

    challenge = vp_library.generate_challenge()
    users[username]["challenge"] = challenge

    return f'''
        <!doctype html>
        <h1>Challenge-Response: Provide Response</h1>
        <form action="/validate-response" method="post">
            Username: {username}<br><input type="hidden" name="username" value="{username}">
            Challenge: <b>{challenge}</b><br>
            OTP: <input type="text" name="otp"><br>
            <br>
            <input type="submit" value="Login">
        </form>
        <p>[ <a href="/">Log-in</a> ]'''


@app.route('/validate-response', methods=['POST'])
def validate_response():
    # Get username, password and OTP
    username = request.form['username']
    otp = request.form['otp']

    # Napake so zgolj v pomoč pri razhroščevanju
    # V produkciji bi povedali le, da prijava ni uspela
    # ne pa tudi zakaj
    if username not in users:
        message = "Invalid username"

    recomputed = vp_library.generate_response_hmac_256(
        bytes.fromhex(users[username]["key"]),
        users[username]["challenge"])
    if not constant_time.bytes_eq(recomputed.encode("utf8"), otp.encode("utf8")):
        message = "Invalid OTP"

    message = f"Welcome, {username}, provided response was correct."

    return f'''
        <!doctype html>
        <h1>Challenge-Response: Login status</h1>
        <p>{message}
        <p>[ <a href="/">Log-in</a> ]'''


if __name__ == '__main__':
    app.run(debug=True)

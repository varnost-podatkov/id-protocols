from cryptography.hazmat.primitives import constant_time
from flask import Flask, request

import vp_library

app = Flask(__name__)

# Baza uporabnikov
# - Vsak uporabnik bi moral imeti isti kljuc
# - A primer namenoma poenostavljamo
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

    challenge = vp_library.generate_challenge()
    users[username]["challenge"] = challenge

    return f'''
        <form action="/validate-response" method="post">
            Username: {username}<br><input type="hidden" name="username" value="{username}"><br>
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
    otp = request.form['otp']

    # Napake so zgolj v pomoč pri razhroščevanju
    # V produkciji bi povedali le, da prijava ni uspela
    # ne pa tudi zakaj
    assert username in users, "Invalid username"

    recomputed = vp_library.generate_response_hmac_256(
        bytes.fromhex(users[username]["key"]),
        users[username]["challenge"])
    if not constant_time.bytes_eq(recomputed.encode("utf8"), otp.encode("utf8")):
        return "Invalid OTP"

    return f"Welcome, {username}, OTP was correct."


if __name__ == '__main__':
    app.run(debug=True)

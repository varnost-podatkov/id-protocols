from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import HOTP
from flask import Flask, request

app = Flask(__name__)

# Uporabniki
# - Vsak uporabnik bi moral imeti svoj kljuc, a namenoma poenostavljamo
users = {
    'ana': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "counter": 0},
    'bor': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "counter": 0},
    'cene': {
        "key": "581f22628ce7b73da43abfceb41c94a5",
        "counter": 0},
}


@app.route('/', methods=['GET'])
def login():
    return '''
        <!doctype html>
        <h1>HOTP Login</h1>
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
    username = request.form['username']
    otp = request.form['otp']

    message = 'Invalid username or OTP.'

    if username in users:
        hotp = HOTP(bytes.fromhex(users[username]["key"]), 6, SHA1())
        for counter in range(users[username]["counter"], users[username]["counter"] + 10):
            try:
                hotp.verify(otp.encode("utf8"), counter)
                users[username]["counter"] = counter + 1
                message = f"Welcome, {username}, OTP was correct. Key counter incremented to {counter}."
                break
            except InvalidToken:
                pass

    return f'''
        <!doctype html>
        <h1>HOTP Login status</h1>
        <p>{message}
        <p>[ <a href="/">Log-in</a> ]
    '''


if __name__ == '__main__':
    app.run(debug=True)

from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import HOTP
from flask import Flask, request

app = Flask(__name__)

# Uporabniki
# - Vsak uporabnik bi moral imeti isti kljuc
# - A primer namenoma poenostavljamo
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
        <form action="/validate" method="post">
            Username: <input type="text" name="username"><br>
            OTP: <input type="text" name="otp"><br>
            <br>
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/validate', methods=['POST'])
def validate_user_pass():
    username = request.form['username']
    otp = request.form['otp']

    if username in users:
        hotp = HOTP(bytes.fromhex(users[username]["key"]), 6, SHA1())
        for i in range(users[username]["counter"], users[username]["counter"] + 10):
            try:
                counter = users[username]["counter"] + i
                hotp.verify(otp.encode("utf8"), counter)
                users[username]["counter"] = counter + 1
                return f"Welcome, {username}, OTP was correct. Key counter incremented to {counter}."
            except InvalidToken:
                pass

        return "Invalid OTP."
    return 'Invalid username.'


if __name__ == '__main__':
    app.run(debug=True)

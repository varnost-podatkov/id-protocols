# Import necessary modules
import time

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from flask import Flask, request

# Create a Flask web application
app = Flask(__name__)

# Hardcoded username and password
valid_credentials = {'username': 'admin', 'password': 'admin123'}


# Endpoint for presenting a username/password dialog
@app.route('/login', methods=['GET'])
def login():
    return '''
        <form action="/validate-user-pass" method="post">
            <p>Username: <input type="text" name="username"></p>
            <p>Password: <input type="password" name="password"></p>
            <p><input type="submit" value="Login"></p>
        </form>
    '''


# Endpoint for checking the validity of the provided username/password pair
@app.route('/validate-user-pass', methods=['POST'])
def validate_user_pass():
    # Get username and password from the form
    entered_username = request.form['username']
    entered_password = request.form['password']

    # Check if the provided credentials are valid
    if entered_username == valid_credentials['username'] and entered_password == valid_credentials['password']:
        return '''
            <form action="/validate-otp" method="post">
                <p>OTP: <input type="text" name="otp"></p>
                <p><input type="submit" value="Login"></p>
            </form>
        '''
    else:
        return 'Invalid username or password.'


@app.route('/validate-otp', methods=['POST'])
def validate_otp():
    # Get username and password from the form
    entered_otp = request.form['otp']

    # Check if the provided credentials are valid
    totp = TOTP(bytes.fromhex("581f22628ce7b73da43abfceb41c94a5"), 6, SHA256(), 30)
    try:
        totp.verify(entered_otp.encode("ascii"), int(time.time()))
        return "Welcome, the OTP was correct."
    except InvalidToken:
        return "Invalid OTP."


# Run the application if the script is executed
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request

import vp_library

app = Flask(__name__)

# Baza uporabnikov
# - Kljuc predstavlja uporabnika, vrednosti pa sta par (sol, zgoščeno geslo)
# - Podan je primer za Ano in za geslo "vp"
_salt, _hashed = vp_library.hash_password("vp")
users = {
    'ana': (_salt, _hashed),
}


@app.route('/', methods=['GET'])
def login():
    return '''
        <!doctype html>
        <h1>Log in</h1>
        <form action="/validate" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <br>
            <input type="submit" value="Login">
        </form>
        <p>[
            <a href="/">Log-in</a> |
            <a href= "/register">Register</a>
        ]'''


@app.route('/register', methods=['GET'])
def register():
    return '''
        <!doctype html>
        <h1>Register</h1>
        <form action="/register" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <br>
            <input type="submit" value="Register">
        </form>
        <p>[
            <a href="/">Log-in</a> |
            <a href= "/register">Register</a>
        ]'''


@app.route('/register', methods=['POST'])
def register_save():
    username = request.form['username']
    password = request.form['password']

    if username in users:
        return "Username already taken."

    salt, hashed = vp_library.hash_password(password)
    users[username] = salt, hashed

    return f'''
        <!doctype html>
        <h1>Register</h1>
        <p>Welcome, {username}, the registration was successful.
        <p>[
            <a href="/">Log-in</a> |
            <a href= "/register">Register</a>
        ]'''



@app.route('/validate', methods=['POST'])
def validate_user_pass():
    username = request.form['username']
    password = request.form['password']

    msg = f"Welcome, {username}, the passsword was correct."
    if not (username in users and vp_library.verify_password(password, *users[username])):
        msg = "Invalid username/password"

    return f'''
        <!doctype html>
        <h1>Login status</h1>
        <p>{msg}
        <p>[
            <a href="/">Log-in</a> |
            <a href= "/register">Register</a>
        ]'''


if __name__ == '__main__':
    app.run(debug=True)

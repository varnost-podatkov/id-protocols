from flask import Flask, request

import vp_library

app = Flask(__name__)

# Baza uporabnikov
# - Kljuc predstavlja uporabnika, vrednosti pa sta par (sol, zgosceno geslo)
# - Podan je primer za Ano in za geslo "vp"
_salt, _hashed = vp_library.hash_password("vp")
users = {
    'ana': (_salt, _hashed),
}


@app.route('/', methods=['GET'])
def login():
    return '''
        <form action="/validate" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <br>
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/register', methods=['GET'])
def register():
    return '''
        <form action="/register" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <br>
            <input type="submit" value="Register">
        </form>
    '''


@app.route('/register', methods=['POST'])
def register_save():
    username = request.form['username']
    password = request.form['password']

    if username in users:
        return "Username already taken."

    salt, hashed = vp_library.hash_password(password)
    users[username] = salt, hashed

    return f"Welcome, {username}, the registration was successful."


@app.route('/validate', methods=['POST'])
def validate_user_pass():
    username = request.form['username']
    password = request.form['password']

    if not (username in users and vp_library.verify_password(password, *users[username])):
        return "Invalid username/password"

    return f"Welcome, {username}, the passsword was correct."


if __name__ == '__main__':
    app.run(debug=True)

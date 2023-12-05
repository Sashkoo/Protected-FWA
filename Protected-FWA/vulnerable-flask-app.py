from flask import Flask,jsonify,render_template_string,request,Response,render_template, send_from_directory, session
import subprocess, os, sqlite3
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename

from markupsafe import escape



app = Flask(__name__)
app.config['UPLOAD_FOLDER']="/home/kali/Desktop/upload"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route('/')
def home():
    return "<h1>Vulnerable app</h1>"

#xss
@app.route("/xss")
def index():
    name = request.args.get('name', '')
    safe_name = escape(name)
    return f"Hello, {safe_name}!"

#idor
data = {
    '1': 'Vania',
    '2': 'Jacob',
    '3': 'Alex'
}
@app.route('/users')
def get_user():
    user_id = request.args.get('id')

    if current_user.is_authenticated:
        if user_id in data:
            return f"User: {data[user_id]}"
        else:
            return "User not found"
    else:
        return "Unauthorized access"

#sqli
@app.route("/user/<string:name>")
def search_user(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM test WHERE username = ?", (name,))
    data = cur.fetchall()
    con.close()
    
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    
    return jsonify(data=data), 200

#OS injection
@app.route("/os_inj")
def page():
    hostname = request.args.get("hostname")
    
    try:
        output = subprocess.check_output(["hostnamectl", "status", hostname])
        return output.decode(), 200
    except subprocess.CalledProcessError:
        return "Error", 500

#Path traversal
@app.route("/read_file")
def read_file():
    filename = request.args.get('filename')

    if not is_safe_filename(filename):
        return jsonify(error="Invalid filename"), 400

    file_path = os.path.join(app.root_path, 'uploads', filename)

    if not os.path.exists(file_path):
        return jsonify(error="File not found"), 404

    with open(file_path, "r") as file:
        data = file.read()

    return jsonify(data=data), 200

def is_safe_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf'}

#Brute force
app.secret_key = 'secret_ley_Asdada8dsaaad9as'
MAX_LOGIN_ATTEMPTS = 3

@app.route('/login', methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if check_credentials(username, password):
        reset_login_attempts()
        return jsonify(data="Login successful"), 200
    else:
        increment_login_attempts()

        if get_login_attempts() >= MAX_LOGIN_ATTEMPTS:
            return jsonify(data="Account locked. Too many login attempts."), 403
        else:
            return jsonify(data="Login unsuccessful"), 403

def check_credentials(username, password):
    return "admin" in username and "superadmin" in password

def increment_login_attempts():
    if 'login_attempts' not in session:
        session['login_attempts'] = 0
    session['login_attempts'] += 1

def get_login_attempts():
    return session.get('login_attempts', 0)

def reset_login_attempts():
    session.pop('login_attempts', None)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8081)

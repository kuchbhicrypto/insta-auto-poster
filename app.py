"""

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# === Define Full DB Path ===
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

# === Setup DB if not exists ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# === Routes ===

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except:
            return "User already exists!"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add new route to database for scheduled uploads
def init_post_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS uploads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    filename TEXT,
                    filetype TEXT,
                    schedule_time TEXT
                )''')
    conn.commit()
    conn.close()

init_post_db()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            file = request.files['file']
            filetype = request.form['filetype']
            schedule_time = request.form['schedule_time']
            username = session['user']

            if file and allowed_file(file.filename):
                filename = f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                print("Saving to DB:", username, filename, filetype, schedule_time)

                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("INSERT INTO uploads (username, filename, filetype, schedule_time) VALUES (?, ?, ?, ?)",
                          (username, filename, filetype, schedule_time))
                conn.commit()
                conn.close()

                print("Data saved successfully ✅")
                return "File uploaded and scheduled successfully!"
            else:
                return "Invalid file type!"
        except Exception as e:
            print("Error while uploading:", e)
            return f"Error: {e}"

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)



#this works well
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# === Define Full DB Path ===
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

# === Setup users table ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

# === Setup uploads table ===
def init_post_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS uploads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    filename TEXT,
                    filetype TEXT,
                    schedule_time TEXT
                )''')
    conn.commit()
    conn.close()

# Initialize both tables at startup
init_db()
init_post_db()

# === Routes ===

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except:
            return "User already exists!"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads WHERE username=?", (session['user'],))
    uploads = c.fetchall()
    conn.close()

    return render_template('dashboard.html', username=session['user'], uploads=uploads)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# === Upload Config ===
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            file = request.files['file']
            filetype = request.form['filetype']
            schedule_time = request.form['schedule_time']
            username = session['user']

            if file and allowed_file(file.filename):
                filename = f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                # Save to DB
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("INSERT INTO uploads (username, filename, filetype, schedule_time) VALUES (?, ?, ?, ?)",
                          (username, filename, filetype, schedule_time))
                conn.commit()
                conn.close()

                print("Data saved successfully ✅")
                return "File uploaded and scheduled successfully!"
            else:
                return "Invalid file type!"
        except Exception as e:
            print("Error while uploading:", e)
            return f"Error: {e}"

    return render_template('upload.html')

# === Test Route to See All Uploads ===
@app.route('/view_uploads')
def view_uploads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads")
    uploads = c.fetchall()
    conn.close()

    html = "<h2>All Scheduled Uploads</h2><ul>"
    for u in uploads:
        html += f"<li><b>{u[1]}</b> scheduled <i>{u[2]}</i> at {u[4]}</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
"""

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import requests  # For Gemini API

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# === Define DB Path ===
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

# === Setup users table ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

# === Setup uploads table ===
def init_post_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS uploads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    filename TEXT,
                    filetype TEXT,
                    schedule_time TEXT,
                    caption TEXT,
                    hashtags TEXT,
                    audio TEXT,
                    status TEXT DEFAULT 'pending'
                )''')
    conn.commit()
    conn.close()

init_db()
init_post_db()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except:
            return "User already exists!"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads WHERE username=?", (session['user'],))
    uploads = c.fetchall()
    conn.close()

    return render_template('dashboard.html', username=session['user'], uploads=uploads)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# === Gemini API Function ===
def generate_caption_hashtags_audio(file_path):
    # This is just a placeholder — actual implementation will be in Gemini script
    return ("Your motivational caption 🌟", "#luxury #dreamlife", "trending_audio.mp3")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            file = request.files['file']
            filetype = request.form['filetype']
            schedule_time = request.form['schedule_time']
            username = session['user']

            if file and allowed_file(file.filename):
                filename = f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                # === Call Gemini for caption & hashtags
                caption, hashtags, audio = generate_caption_hashtags_audio(filepath)

                # Save to DB
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('''INSERT INTO uploads 
                    (username, filename, filetype, schedule_time, caption, hashtags, audio)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (username, filename, filetype, schedule_time, caption, hashtags, audio))
                conn.commit()
                conn.close()

                print("Uploaded & Gemini AI captions generated ✅")
                return "File uploaded and scheduled with caption/hashtags!"
            else:
                return "Invalid file type!"
        except Exception as e:
            print("Upload error:", e)
            return f"Error: {e}"

    return render_template('upload.html')

@app.route('/view_uploads')
def view_uploads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads")
    uploads = c.fetchall()
    conn.close()

    html = "<h2>All Scheduled Uploads</h2><ul>"
    for u in uploads:
        html += f"<li><b>{u[1]}</b> scheduled <i>{u[2]}</i> at {u[4]}<br>Caption: {u[5]}<br>Hashtags: {u[6]}</li>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

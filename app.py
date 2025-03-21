from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )''')

# Insert Form Data into Database
def insert_submission(name, email, message):
    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO submissions (name, email, message) VALUES (?, ?, ?)", 
                     (name, email, message))

# Retrieve Submissions
def get_submissions():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.execute("SELECT * FROM submissions")
        return cursor.fetchall()

# Home Page (Form)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        insert_submission(name, email, message)
        return redirect(url_for('home'))
    return render_template('index.html', logo_url=url_for('static', filename='logo.png'))

# View Submissions
@app.route('/submissions')
def submissions():
    entries = get_submissions()
    return render_template('submissions.html', entries=entries)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)

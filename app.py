from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'resumego_secret_key'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="student",
    database="resumego_db"
)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        contact = request.form.get('contact')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return "Passwords do not match!"

        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return "Email already registered!"

        cursor.execute(
            "INSERT INTO users (fullname, email, contact, password) VALUES (%s, %s, %s, %s)",
            (fullname, email, contact, password)
        )
        mydb.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mydb.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user[0]   # store user id
            return redirect(url_for('info'))
        else:
            return "Invalid credentials! Please try again."

    return render_template('login.html')

@app.route('/info')
def info():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('info.html')


@app.route('/templates')
def templates():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('templates.html')

@app.route('/template<int:template_id>')
def show_template(template_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    valid_templates = [1, 2, 3, 4]
    if template_id not in valid_templates:
        return "Template not found", 404

    return render_template(f'template{template_id}.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

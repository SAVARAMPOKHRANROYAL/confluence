from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)


# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Add your MySQL root password here if set
app.config['MYSQL_DB'] = 'pok'

mysql = MySQL(app)

@app.route("/")
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, client_name, environment FROM clients")
    items = cursor.fetchall()
    cursor.close()
    return render_template("index.html", items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():     
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_name = %s AND password = %s', (name, password))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return render_template("devops.html")
        else:
            return "Invalid username or password."
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''INSERT INTO users (user_name, password) VALUES (%s, %s)''', (name, password))
            mysql.connection.commit()
            return render_template("login.html")
        except Exception as e:
            mysql.connection.rollback()
            return str(e)
        finally:
            cursor.close()
    return render_template("signup.html")

@app.route('/logout')
def logout():
    return render_template("logout.html")

@app.route("/admindata")
def data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, client_name, environment FROM clients")
    items = cursor.fetchall()
    cursor.close()
    return render_template("adminindex.html", items=items)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        client_name = request.form['Client_Name']
        environment = request.form['Environment']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''UPDATE clients SET client_name = %s, environment = %s WHERE id = %s''', (client_name, environment, id))
            mysql.connection.commit()
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, client_name, environment FROM clients")
            items = cursor.fetchall()
            cursor.close()
            return render_template("adminindex.html", items=items)
        except Exception as e:
            mysql.connection.rollback()
            return str(e)
        finally:
            cursor.close()
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, client_name, environment FROM clients WHERE id = %s', (id,))
        user = cursor.fetchone()
        cursor.close()
        return render_template("edit.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)

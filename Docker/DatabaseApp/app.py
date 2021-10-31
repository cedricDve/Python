from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import pymysql.cursors
import json

app = Flask(__name__)
# MySQL Config variables
app.config['MYSQL_HOST'] = 'mysqldb'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'p@ssw0rd1'
app.config['MYSQL_DB'] = 'mainDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/users')
def get_widgets() :
    # Connect to the database
    connection = pymysql.connect(host='mysqldb',
                                user='root',
                                password='p@ssw0rd1',
                                database='mainDB',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
          
        return json.dumps(users)

@app.route('/scores')
def get_scores():
    # Connect to the database
    connection = pymysql.connect(host='mysqldb',
                                user='root',
                                password='p@ssw0rd1',
                                database='mainDB',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM scores")
            scores = cursor.fetchall()
          
        return json.dumps(scores)

@app.route('/initdb')
def db_init():
    connection = pymysql.connect(host='mysqldb',
                                user='root',
                                password='p@ssw0rd1',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("DROP DATABASE IF EXISTS mainDB")
            cursor.execute("CREATE DATABASE mainDB")
            cursor.execute("DROP DATABASE IF EXISTS spaceGame")
            cursor.execute("CREATE DATABASE spaceGame")
            cursor.close()
        connection.commit()

    db_connection = pymysql.connect(host='mysqldb',
                            user='root',
                            password='p@ssw0rd1',
                            database='spaceGame',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    with db_connection:
        with db_connection.cursor() as cursor:

            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), email VARCHAR(255), password VARCHAR(255), UNIQUE KEY `email` (`email`))")
            cursor.execute("DROP TABLE IF EXISTS scores")
            cursor.execute("CREATE TABLE scores (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), score INT, level INT)")
            cursor.close()
        db_connection.commit()

 

    cur = mysql.connection.cursor() 
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), email VARCHAR(255), password VARCHAR(255), UNIQUE KEY `email` (`email`))")
    mysql.connection.commit()

    return redirect(url_for('home'))



   

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")



if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True, host ='0.0.0.0')

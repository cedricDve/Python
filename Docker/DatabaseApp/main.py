import pymysql.cursors
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, Docker!'

@app.route('/widgets')
def get_widgets() :
    # Connect to the database
    connection = pymysql.connect(host='mysqldb',
                                user='root',
                                password='p@ssw0rd1',
                                database='inventory',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM widgets")

            row_headers=[x[0] for x in cursor.description] #this will extract row headers

            results = cursor.fetchall()
            json_data=[]
            for result in results:
                json_data.append(dict(zip(row_headers,result)))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            cursor.close()

    return json.dumps(json_data)

@app.route('/initdb')
def db_init():
    connection = pymysql.connect(host='mysqldb',
                                user='root',
                                password='p@ssw0rd1',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("DROP DATABASE IF EXISTS inventory")
            cursor.execute("CREATE DATABASE inventory")
            cursor.close()

    connection = pymysql.connect(host='mysqldb',
                            user='root',
                            password='p@ssw0rd1',
                            database='inventory',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    with connection:
    # Create table Widgets
        with connection.cursor() as cursor:

            cursor.execute("DROP TABLE IF EXISTS widgets")
            cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
            cursor.close()
    # Create table Users
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), email VARCHAR(255), password VARCHAR(255), UNIQUE KEY `email` (`email`))")
            cursor.close()

    return 'init database'

if __name__ == "__main__":
  app.run(debug= True, host ='0.0.0.0')
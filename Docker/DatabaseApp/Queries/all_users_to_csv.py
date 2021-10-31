import pymysql.cursors
import csv

def db_init(database_name):
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='p@ssw0rd1',
                                charset='utf8mb4',
                                database= database_name,
                                cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
           
            users = cursor.fetchall()
            print(users)
          

            file = csv.writer(open(f'./all-user-{database_name}.csv', 'w',encoding='utf-8'))
            file.writerows(users)       
           
database_name = input("Database name: ")
db_init(database_name)
    


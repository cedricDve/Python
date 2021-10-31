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
            # Write output to csv
            with open('exported-from-sql-query.csv', 'w') as csvfile:
                column_names = list(users[0].keys()) #  or manual list
                myCsvWriter = csv.DictWriter(csvfile,
                                            fieldnames = column_names)
                myCsvWriter.writeheader()

                # write the rows.                 
                for row in users:# Note: the results are now provided by pymysql
                    myCsvWriter.writerow(row)
           
database_name = input("Database name: ")
db_init(database_name)
    


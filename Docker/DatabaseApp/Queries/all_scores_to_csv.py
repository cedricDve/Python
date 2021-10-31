import pymysql.cursors
import csv

def db_init():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='p@ssw0rd1',
                                charset='utf8mb4',
                                database= "spaceGame",
                                cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM scores")
            scores = cursor.fetchall()
            print(scores)         
            # Write output to csv
            with open('exported-from-mysql-scores.csv', 'w') as csvfile:
                column_names = list(scores[0].keys()) #  or manual list
                myCsvWriter = csv.DictWriter(csvfile,
                                            fieldnames = column_names)
                myCsvWriter.writeheader()

                # write the rows.                 
                for row in scores:# Note: the results are now provided by pymysql
                    myCsvWriter.writerow(row)
           
db_init()
    


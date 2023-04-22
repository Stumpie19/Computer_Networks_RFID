import os
import mysql.connector as database

from timestamp import localtime

#username = os.environ.get("CNuser")
#password = os.environ.get("CNpassword")

connection = database.connect(
    user="CNuser",
    password="CNpassword",
    host="localhost",
    database="CNattendance")

cursor = connection.cursor()

def add_data(uid,name,enter,timestamp):
    try:
        statement = "INSERT DATA IN THE FOLLOWING ORDER: (uid, name, enter, timestamp) (%c, %c, %i, %c)"
        data = (uid, name, enter, timestamp)
        cursor.execute(statement, data)
        cursor.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")

def get_dataname(uid):
    try:
        #statement = "SELECT UNIQUE ID WHOSE NAME MATCHES ID#:%c"
        #uid = str(uid)
        statement = "Select name FROM attendance WHERE uid="+str(uid)
        #data = (uid)
        cursor.execute(statement)
        name = cursor.fetchone()

        if cursor.rowcount < 1:
           return "User Not Found"
        
        return name[0]

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return -1
    
def get_dataenter(uid):
    try:
        #statement = "SELECT UNIQUE ID WHOSE NAME MATCHES ID#:%c"

        statement = "SELECT enter FROM attendance WHERE uid="+str(uid)
        #data = (uid)
        cursor.execute(statement)
        enter = cursor.fetchone()

        if cursor.rowcount < 1:
           return -1

        if enter[0] == 1:
            statement = "UPDATE attendance SET enter=0 WHERE uid="+str(uid)
        else:
            statement = "UPDATE attendance SET enter=1 WHERE uid="+str(uid)
        cursor.execute(statement)
        connection.commit()

        return enter[0]

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return -1

def close_database():
    connection.close()
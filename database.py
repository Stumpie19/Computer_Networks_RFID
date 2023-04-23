import os
import mysql.connector as database

from timestamp import localtime


connection = database.connect(
    user="CNuser",
    password="CNpassword",
    host="localhost",
    database="CNattendance")

cursor = connection.cursor()

def add_data(uid,name,enter,timestamp_in, timestamp_out):
    try:
        statement = "INSERT INTO attendance (uid, name, enter, timestamp_in, timestamp_out) ("+str(uid)+","+str(name)+","+str(enter)+","
            +str(timestamp_in)+","+str(timestamp_out)+")"
        cursor.execute(statement)
        connection.commit()
        print("Successfully added entry to database")
        return 0
    except database.Error as e:
        print(f"Error adding entry to database: {e}")
        return -1

def get_dataname(uid):
    try:
        statement = "Select name FROM attendance WHERE uid="+str(uid)
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

        statement = "SELECT enter FROM attendance WHERE uid="+str(uid)
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

def delete_data(uid):
    try:
        statement = f"DELETE FROM attendance WHERE uid = '{uid}'"
        cursor.execute(statement)
        connection.commit()
    except database.Error as e:
        print(f"Error deleting entry from database: {e}")

def update_timestamp_in(uid, timestamp_in):
    try:
        #print(timestamp_in)
        statement = f"UPDATE attendance SET timestamp_in = '{timestamp_in}' WHERE uid = '{uid}'"
        cursor.execute(statement)
        connection.commit()
    except database.Error as e:
        print(f"Error updating timestamp in database: {e}")

def update_timestamp_out(uid, timestamp_out):
    try:
        statement = f"UPDATE attendance SET timestamp_out = '{timestamp_out}' WHERE uid = '{uid}'"
        cursor.execute(statement)
        connection.commit()
    except database.Error as e:
        print(f"Error updating timestamp in database: {e}")

def close_database():
    connection.close()

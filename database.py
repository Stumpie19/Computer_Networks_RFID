import os
import mysql.connector as database

#Connect to MySQL Database
connection = database.connect(
    user="CNuser",
    password="CNpassword",
    host="localhost",
    database="CNattendance")

#Create a cursor
cursor = connection.cursor()

#Adding entry into database
def add_data(uid,name,enter,timestamp_in, timestamp_out):
    try:
        statement = "INSERT INTO attendance (uid, name, enter, timestamp_in, timestamp_out) VALUES ('"+str(uid)+"','"+str(name)+"',"+str(enter)+",'"+str(timestamp_in)+"','"+str(timestamp_out)+"')"

        #Execute above statement
        cursor.execute(statement)
        #Commit to database
        connection.commit()

        print("uid = "+str(uid))
        print("Successfully added entry to database")
        return 0
    except database.Error as e:
        print(f"Error adding entry to database: {e}")
        return -1

#Pulling name from database
def get_dataname(uid):
    try:
        statement = "Select name FROM attendance WHERE uid="+str(uid)

        #Execute above statement
        cursor.execute(statement)
        #Fetching a row in the MySQL database
        name = cursor.fetchone()

        if cursor.rowcount < 1:
           return "User Not Found"
        
        return name[0]

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return -1
    
#Pulling in/out from database
def get_dataenter(uid):
    try:

        statement = "SELECT enter FROM attendance WHERE uid="+str(uid)

        #Execute above statement        
        cursor.execute(statement)
        #Fetch a row in the MySQL Database
        enter = cursor.fetchone()

        if cursor.rowcount < 1:
           return -1

        if enter[0] == 1:
            statement = "UPDATE attendance SET enter=0 WHERE uid="+str(uid)
        else:
            statement = "UPDATE attendance SET enter=1 WHERE uid="+str(uid)
        
        #Execute above statement
        cursor.execute(statement)
        #Commit changes
        connection.commit()

        return enter[0]

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return -1

#Deleting entry from database
def delete_data(uid):
    try:
        statement = f"DELETE FROM attendance WHERE uid = '{uid}'"

        #Execute above statement
        cursor.execute(statement)
        #Commit to database
        connection.commit()

        print("uid = "+str(uid))
        print("Successfully deleted entry to database")
    except database.Error as e:
        print(f"Error deleting entry from database: {e}")

#Update time in
def update_timestamp_in(uid, timestamp_in):
    try:
        statement = f"UPDATE attendance SET timestamp_in = '{timestamp_in}' WHERE uid = '{uid}'"

        #Execute above statement
        cursor.execute(statement)
        #Commit to database
        connection.commit()

    except database.Error as e:
        print(f"Error updating timestamp in database: {e}")

#Update time out
def update_timestamp_out(uid, timestamp_out):
    try:
        statement = f"UPDATE attendance SET timestamp_out = '{timestamp_out}' WHERE uid = '{uid}'"

        #Execute above statement
        cursor.execute(statement)
        #Commit to database
        connection.commit()

    except database.Error as e:
        print(f"Error updating timestamp in database: {e}")

#Close database
def close_database():
    connection.close()

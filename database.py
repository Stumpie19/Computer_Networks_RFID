import os
import mysql.connector as database

from timestamp import localtime

username = os.environ.get("CNuser")
password = os.environ.get("CNpassword")

connection = database.connect(
	user=username,
	password=password,
	host=localhost,
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

def get_data(name):
	try:
		statement = "SELECT UNIQUE ID WHOSE NAME MATCHES ID#:%c"
		data = (uid)
		cursor.execute(statement, data)
		for (uid) in cursor:
			print(f"Successfully retrieved {uid}, {name}")
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")

add_data("123456789012", "Jacob", 1, localtime)
get_data("123456789012")

connection.close()
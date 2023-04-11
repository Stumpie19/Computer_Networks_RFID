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

def get_datauid(uid):
	try:
		statement = "SELECT uid FROM database WHERE uid=%c"
		data = (uid,)
		cursor.execute(statement, data)
		for (uid) in cursor:
			print(f"Successfully retrieved {uid}")
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")
	return uid

def get_dataname(uid):
	try:
		statement = "SELECT name FROM database WHERE uid=%c"
		data = (uid,)
		cursor.execute(statement, data)
		for (uid, name) in cursor:
			print(f"Successfully retrieved {uid}, {name}")
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")
	return name

def get_dataenter(uid):
	try:
		statement = "SELECT enter FROM database WHERE uid=%c"
		data = (uid,)
		cursor.execute(statement, data)
		for (uid, enter) in cursor:
			print(f"Successfully retrieved {uid},{enter}")
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")
	return enter

def get_data(uid):
	try:
		statement = "SELECT uid, name, enter FROM database WHERE uid=%c"
		data = (uid,)
		cursor.execute(statement, data)
		for (uid, name, enter) in cursor:
			print(f"Successfully retrieved {uid}, {name}, {enter}")
	except database.Error as e:
		print(f"Error retrieving entry from database: {e}")


add_data("123456789012", "Jacob", 1, localtime)
get_data("123456789012")

connection.close()
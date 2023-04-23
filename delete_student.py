import RFID_Driver
import RPi.GPIO as GPIO
import mysql.connector as database

while True:
    try:
        username = input("Username:")
        password = input("Password:")
        connection = database.connect(
            user=username,
            password=password,
            host="localhost",
            database="CNattendance")

        cursor = connection.cursor()

        print("Scan RFID tag:")
        reader = RFID_Driver.RFID_READER()
        try:
            uid = reader.get_id()
        finally:
            GPIO.cleanup()

        try:
            statement = f"DELETE FROM attendance WHERE uid = '{uid}'"
            cursor.execute(statement)
            connection.commit()
            print(f"Student successfully removed from database")
        except database.Error as e:
            print(f"Error deleting student from database: {e}")
        finally:
            connection.close()
            break
        
    except database.Error:
        print("Incorrect username or password")
    
    except:
        break

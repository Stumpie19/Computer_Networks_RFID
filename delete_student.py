import RFID_Driver
import RPi.GPIO as GPIO
import mysql.connector as database

while True:
    try:
        #Prompt user for database login credentials
        username = input("Username:")
        password = input("Password:")
        
        #Connect to MySQL Database
        connection = database.connect(
            user=username,
            password=password,
            host="localhost",
            database="CNattendance")

        #Create a cursor
        cursor = connection.cursor()

        print("Scan RFID tag:")
        
        #Initialize RFID Reader/Driver
        reader = RFID_Driver.RFID_READER()
        
        try:
            #Fetch RFID
            uid = reader.get_id()
        finally:
            GPIO.cleanup()

        try:
            statement = f"DELETE FROM attendance WHERE uid = '{uid}'"
            
            #Execute above statement
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

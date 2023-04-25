from database import add_data
import RFID_Driver
import RPi.GPIO as GPIO
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

#Initialize LCD
lcd = LCD()
def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

#Display "Scan RFID tag" on LCD
lcd.text("Scan RFID tag", 1)

print("Scan RFID tag:")

#Initialize RFID Reader/Driver
reader = RFID_Driver.RFID_READER()

try:
    #Fetch RFID
    uid = reader.get_id()
finally:
    GPIO.cleanup()

lcd.clear()

#Display "Enter name" on LCD
lcd.text("Enter name", 1)

name = input("Enter name:")

#Add an entry to database
result = add_data(uid, name, 0, int(time.time()), int(time.time()))

if result == 0:
    print(f"Successfully added {name} to database")
    
    lcd.clear()

    #Display confirmation message on LCD
    lcd.text(str(name), 1)
    lcd.text("added to DB", 2)

else:
    print("Error adding student to database")
    
    lcd.clear()

    #Display error message on LCD
    lcd.text("Error", 1)

#Wait 5 seconds before clearing LCD
time.sleep(5)
lcd.clear()

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

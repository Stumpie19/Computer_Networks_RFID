from database import add_data
import RFID_Driver
import RPi.GPIO as GPIO
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

lcd = LCD()
def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
lcd.text("Scan RFID tag", 1)

print("Scan RFID tag:")

reader = RFID_Driver.RFID_READER()
try:
    uid = reader.get_id()
finally:
    GPIO.cleanup()

lcd.clear()
lcd.text("Enter name", 1)
name = input("Enter name:")
result = add_data(uid, name, 0, int(time.time()), int(time.time()))

if result == 0:
    print(f"Successfully added {name} to database")
    
    lcd.clear()
    lcd.text(str(name), 1)
    lcd.text("added to DB", 2)

else:
    print("Error adding student to database")
    
    lcd.clear()
    lcd.text("Error", 1)

time.sleep(5)
lcd.clear()
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

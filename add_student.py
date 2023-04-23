from database import add_data
import RFID_Driver
import RPi.GPIO as GPIO
import time


print("Scan RFID tag:")

reader = RFID_Driver.RFID_READER()
try:
    uid = reader.get_id()
finally:
    GPIO.cleanup()
print()

name = input("Enter name:")
add_data(uid, name, 0, time.time())


from signal import signal, SIGTERM, SIGHUP, pause
from database import get_dataname, get_dataenter, update_timestamp_in, update_timestamp_out, close_database
import RFID_Driver
import RPi.GPIO as GPIO
import time
from timestamp import localtime

#From raspberry pi lcd library
from rpi_lcd import LCD


lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
try:
    while True:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        reader = RFID_Driver.RFID_READER()

        try:
            uid = reader.get_id()
            print("\nuid = "+str(uid))
        finally:
            GPIO.cleanup()

        name = get_dataname(uid)
        enter = get_dataenter(uid)
        if enter == 0:
            update_timestamp_in(uid, int(time.time()))
            print("Welcome "+str(name))
            lcd.text("Welcome,", 1)

            #Get name of attendee from database.py
            lcd.text(str(name), 2)
        
        elif enter == 1:
            update_timestamp_out(uid, int(time.time()))
            print("Good-Bye "+str(name))
            lcd.text("Good-Bye", 1)

            #Get name of attendee from database.py
            lcd.text(str(name), 2)
        else:
            lcd.text("Error", 1)
            lcd.text(str(name), 2)
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
    close_database()

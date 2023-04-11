
from signal import signal, SIGTERM, SIGHUP, pause
from database import get_dataname, get_dataenter

#From raspberry pi lcd library
from rpi_lcd import LCD
uid = "1"
get_data(uid)

lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    get_data()
    name1 = get_dataname()
    enter = get_dataenter
    if enter == 1:

        lcd.text("Welcome,", 1)

        #Get name of attendee from database.py
        lcd.text(name1, 2)
    
    else:
        lcd.text("Good-Bye", 1)

        #Get name of attendee from database.py
        lcd.text(name1, 2)
    pause()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
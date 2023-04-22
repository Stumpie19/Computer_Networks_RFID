import RPi.GPIO as GPIO
import RFID_Driver

reader = RFID_Driver.RFID_READER()

try:
	id = reader.get_id()
	print(id)
finally:
	GPIO.cleanup()

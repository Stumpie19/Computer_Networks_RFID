#!/usr/bin/env python
import RFID_Reader
import RPi.GPIO as GPIO
     
class RFID_READER:

  READER = None
  
  def __init__(self):
    self.READER = RFID_Reader.RFID()
    
  #get uid of PICC
  def get_id(self):
    id = self.read_uid()
    while not id:
      id = self.read_uid()
    return id

  #read uid of PICC
  def read_uid(self):
      
      (status, TagType) = self.READER.requestPICC()#Send request command to PICC to move them from idle to ready state
      if status != self.READER.STATUS_OK:#Error Check
          return None
      
      (status, uid_hex) = self.READER.anticollisionPICC()#Perform Anticollision action to get uid of PICC
      if status != self.READER.STATUS_OK:#Error Check 
          return None
      
      #Convert unqiue ID of PICC from hexidecimal to decimal
      uid = 0
      for i in range(0, 5):#loop through uid hexidecimal
          uid = uid * 256 + uid_hex[i]#convert hexidecimal to uid
      return uid

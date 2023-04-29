#!/usr/bin/env python
import RFID_Reader#use class from RFID_Reader.py to get 
import RPi.GPIO as GPIO#Library to control GPIO pins of Raspberry pi

#Class to use fucntions from the RFID class from RFID_Reader in order to request and recieve uid from an RFID tag or PICC
class RFID_READER:

  READER = None#to create object of RFID ckass from RFID_Reader.py
  
  #initialization function that runs when a object of class is created
  def __init__(self):
    self.READER = RFID_Reader.RFID()
    
  #get uid of PICC
  def get_id(self):
    id = self.read_uid()#request and get id from an RFID tag
    while not id:#look until id from tag is valid
      id = self.read_uid()
    return id

  #request and read uid from RFID tag
  def read_uid(self):
      
      (status, TagType) = self.READER.requestPICC()#Send request command to PICC to move them from idle to ready state
      if status != self.READER.STATUS_OK:#Error Check
          return None
      
      (status, uid_hex) = self.READER.anticollisionPICC()#Perform Anticollision action to get uid of PICC
      if status != self.READER.STATUS_OK:#Error Check failed in anticollision function (case if uid is more than 4 Bytes)
          return None
      
      #Convert unqiue ID of PICC from hexidecimal to decimal
      uid = 0
      for i in range(0, (len(uid_hex)-1)):#loop through uid hexidecimal (last Byte of data not part of uid)
          uid = uid * 256 + uid_hex[i]#convert hexidecimal to uid
      return uid

#!/usr/bin/env python

import RPi.GPIO as GPIO
import spidev
import signal
import time

class RFID:
    MAX_LEN = 16 #length constant for Buffer that is used (buffer is 64 bytes)
    
    #Command Constants for MFRC522
    COMMAND_IDLE = 0x00 #command:no action, cancels current command execution
    COMMAND_MEM = 0x01 #command: stores 25 bytes into the internal buffer
    COMMAND_RANDOM_ID = 0x02 #command: generates a 10-byte random ID number
    COMMAND_CALC_CRC = 0x03 #command: activates the CRC coprocessor or performs a self test
    COMMAND_TRANSMIT = 0x04 #command: transmits data from the FIFO buffer
    COMMAND_NO_COMMAND_CHANGE = 0x07 #command: no command change, can be used to modify the CommandReg register bits without affecting the command, for example, the PowerDown bit
    COMMAND_RECIEVE = 0x08 #command: activates the receiver circuits
    COMMAND_TRANSCIEVE = 0x0C #command: transmits data from FIFO buffer to antenna and automatically activates the receiver after transmission
    COMMAND_MF_AUTH = 0x0E #command: performs the MIFARE standard authentication as a reader
    COMMAND_SOFT_RESET = 0x0F #command: resets the MFRC522
    
    #Command Constants for the PICC (RFID Tag)
    COMMAND_PICC_REQA = 0x26 #Request Command
    COMMAND_PICC_WUPA = 0x52 #Wake-Up Command
    COMMAND_PICC_ANTICOLLISION = [0x93,0x20] #Anticollision CL1 Command
    COMMAND_PICC_SELECT = [0x93,0x70] #Select CL1 Command (Only CL1 commands needed since uid of tags used are 4 bytes)
    COMMAND_PICC_HALT = [0x50,0x00] #Halt Command
    COMMAND_PICC_AUTHENT1A = 0x60 #Authentication with Key A Command
    COMMAND_PICC_AUTHENT1B = 0x61 #Authentication with Key B 
    COMMAND_PICC_READ = 0x30 #MIFARE Read Command
    COMMAND_PICC_WRITE = 0xA0 #MIFARE Write Command
    COMMAND_PICC_DECREMENT = 0xC0 #MIFARE Decrement Command
    COMMAND_PICC_INCREMENT = 0xC1 #MIFARE Increment
    COMMAND_PICC_RESTORE = 0xC2 #MIFARE Restore Command
    COMMAND_PICC_TRANSFER = 0xB0 #MIFARE Transfer Command
    
    
    #Status Constants
    STATUS_OK = 0
    STATUS_ERROR = 1
    
    #Registers On MFRC522
    Reserved0 = 0x00
    CommandReg = 0x01
    ComIEnReg = 0x02
    DivlEnReg = 0x03
    ComIrqReg = 0x04
    DivIrqReg = 0x05
    ErrorReg = 0x06
    Status1Reg = 0x07
    Status2Reg = 0x08
    FIFODataReg = 0x09
    FIFOLevelReg = 0x0A
    WaterLevelReg = 0x0B
    ControlReg = 0x0C
    BitFramingReg = 0x0D
    CollReg = 0x0E
    Reserved1 = 0x0F

    Reserved2 = 0x10
    ModeReg = 0x11
    TxModeReg = 0x12
    RxModeReg = 0x13
    TxControlReg = 0x14
    TxASKReg = 0x15
    TxSelReg = 0x16
    RxSelReg = 0x17
    RxThresholdReg = 0x18
    DemodReg = 0x19
    Reserved3 = 0x1A
    Reserved4 = 0x1B
    MfTxReg = 0x1C
    MfRxReg = 0x1D
    Reserved5 = 0x1E
    SerialSpeedReg = 0x1F

    Reserved6 = 0x20
    CRCResultRegMSB = 0x21
    CRCResultRegLSB = 0x22
    Reserved7 = 0x23
    ModWidthReg = 0x24
    Reserved8 = 0x25
    RFCfgReg = 0x26
    GsNReg = 0x27
    CWGsPReg = 0x28
    ModGsPReg = 0x29
    TModeReg = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH = 0x2C
    TReloadRegL = 0x2D
    TCounterValRegH = 0x2E
    TCounterValRegL = 0x2F
    
    Reserved9 = 0x30
    TestSel1Reg = 0x31
    TestSel2Reg = 0x32
    TestPinEnReg = 0x33
    TestPinValueReg = 0x34
    TestBusReg = 0x35
    AutoTestReg = 0x36
    VersionReg = 0x37
    AnalogTestReg = 0x38
    TestDAC1Reg = 0x39
    TestDAC2Reg = 0x3A
    TestADCReg = 0x3B
    Reserved10 = 0x3C
    Reserved11 = 0x3D
    Reserved12 = 0x3E
    Reserved13 = 0x3F
    
    SerialNum = [] #Keep track of serial number
    
    #Function for initialization of object to set up SPI connection with MFRC522
    def __init__(self, bus=0, device=0, pin_mode=10, pin_rst=-1):
        
        #Set up SPI connection
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000 #set speed to 1 MHz

        #SET up GPIO Connection
        gpioMode = GPIO.getmode()
        
        if gpioMode is None:
            GPIO.setmode(pin_mode)
        else:
            pin_mode = gpioMode
            
        if pin_rst == -1:
            if pin_mode == 11:
                pin_rst = 15
            else:
                pin_rst = 22
            
        GPIO.setup(pin_rst, GPIO.OUT)
        GPIO.output(pin_rst, 1)
        self.initRFID() #run initalize fucntion
        
    #Initialize Communication with MFRC522
    def initRFID(self):
        self.reset()#Reset MFRC522

        #Set register to starting values
        self.writeRFID(self.TModeReg, 0x8D)
        self.writeRFID(self.TPrescalerReg, 0x3E)
        self.writeRFID(self.TReloadRegL, 30)
        self.writeRFID(self.TReloadRegH, 0)
        self.writeRFID(self.TxASKReg, 0x40)
        self.writeRFID(self.ModeReg, 0x3D)
        
        self.AntennaOn()#Turn Antenna On
       
    #Soft Reset the MFRC522 Module 
    def reset(self):
        self.writeRFID(self.CommandReg, self.COMMAND_SOFT_RESET)#send reset command to MFRC522

    #Write to a Register on the MFRC522 module
    def writeRFID(self, addr, val):
        val = self.spi.xfer2([(addr << 1) & 0x7E, val])#Write Value to register specified in addr

    #Read from a Register on the MFRC522 module
    def readRFID(self, addr):
        val = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])#Read Value to register specified in addr
        return val[1]
    
    #Clean up instance of class
    def Close_RFID(self):
        self.spi.close()#close SPI Connection
        GPIO.cleanup()#close GPIO Connection

    #Function is change on certain bits of a selected Register to '1'
    def SetBitMask(self, reg, mask):
        tmp = self.readRFID(reg)#read the value in the specified regsiter
        self.writeRFID(reg, tmp | mask)#Mask the value in the specified register to only change certain bits of the register value

    #Function is change on certain bits of a selected Register to '0' 
    def ClearBitMask(self, reg, mask):
        tmp = self.readRFID(reg)#read the value in the specified regsiter
        self.writeRFID(reg, tmp & (~mask))#Mask the value in the specified register to only change certain bits of the register value
        
    #Function Ensures bits Tx1 and Tx2 are on in the TxControlReg (controls the antenna driver pins)
    def AntennaOn(self):
        temp = self.readRFID(self.TxControlReg)#Reads value of TxControlReg
        if (~(temp & 0x03)):#If antenna driver pins are off then turn them on
            self.SetBitMask(self.TxControlReg, 0x03)#Only edit the Tx1 and Tx2 driver pins to on ('1')
            #Tx1 and Tx 2 pins "output signal on pin TX1 (bit 1),Tx2 (bit 2) delivers the 13.56 MHz energy carrier modulated by the transmission data"

    #Function Ensures bits Tx1 and Tx2 are off in the TxControlReg (controls the antenna driver pins)
    def AntennaOff(self):
        self.ClearBitMask(self.TxControlReg, 0x03)#Only edit the Tx1 and Tx2 driver pins to on ('0')
        
    
    #Sends the AnitCollison PICC Command to PICC for PICC to respond with its uid. 
    def anticollisionPICC(self):
        backData = []#for holding data from PICC
        uidCheck = 0#for checking 
        Command = self.COMMAND_PICC_ANTICOLLISION#set command to anticollision command
        
        self.writeRFID(self.BitFramingReg, 0x00)#Reset the bitframing Register

        (status, backData, backBits) = self.sendToPICC(Command)#Send Command to PICC
       
        if (status == self.STATUS_OK):#if status is okay 
            i = 0
            if len(backData) == 5:#if length of uid is 5
                for i in range(4): #loop through uid data to check validity of data
                    uidCheck = uidCheck ^ backData[i] #exclusive or
                if uidCheck != backData[4]: #Error if last Byte of backData doesn't equal exclusive error of first 4 Bytes(means uid is greater than 4 Bytes)
                    status = self.STATUS_ERROR
            else: #if data back is not 5 Bytes
                status = self.STATUS_ERROR
        
        return (status, backData)
    
    #Send data to PICC using a command for the MFRC522
    def sendToPICC(self, sendData):
        command = self.COMMAND_TRANSCIEVE#set the command to transcieve command
        backData = [] #for holding data from PICC
        backLen = 0  #amount of bits of data from PICC
        status = self.STATUS_ERROR #set status to error
        irqEn = 0x77 #Bit to set in comIRQReg before transcieving command
        waitIRq = 0x30 #Active bits of comIRQReg if command successfully sent to PICC
        lastBits = None #amount of bits of data used in last byte
        n = 0 #variable for reading from registers

        self.writeRFID(self.ComIrqReg, irqEn | 0x80)#Set bits in interrupt request bits (7 bit is indicate marked bits are set)
        self.ClearBitMask(self.ComIrqReg, 0x80)#Clear bit 7 to indicate marked bits are cleared in interrupt request register
        
        self.SetBitMask(self.FIFOLevelReg, 0x80)#Set Bit 7 of FIFOLevelReg to fluff FIFO buffer

        self.writeRFID(self.CommandReg, self.COMMAND_IDLE)#Clear active command

        for i in range(len(sendData)):#Set Command to send to PICC in FIFO Data Buffer
            self.writeRFID(self.FIFODataReg, sendData[i])

        self.writeRFID(self.CommandReg, command)#Execute transcieve command

        self.SetBitMask(self.BitFramingReg, 0x80)#Set Bit 7 of BitFramingReg to active to start transmission of data to PICC

        i = 2500#counter for exit loop
        while True:
            n = self.readRFID(self.ComIrqReg)#read comIrqReg  
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & waitIRq)):#read until interrations runs out, TCounterValReg timer get to 0 or, only bits for transmission ended, data stream ended, and command ended bits are all '1'
                break#break loop

        self.ClearBitMask(self.BitFramingReg, 0x80)#Set Bit 7 of BitFramingReg to active to disable transmission of data to PICC

        if i != 0:#if iterations did not run out as exit condition
            if (self.readRFID(self.ErrorReg) & 0x1A) == 0x00:#Read error register and check bits for buffer overflow, bit collision detected, and parity check failed. If any a 1 then error 
                status = self.STATUS_OK

                if n & irqEn & 0x01:#Check Error if timer got to 0 
                    status = self.STATUS_ERROR

                n = self.readRFID(self.FIFOLevelReg)#get number of bits stored in the FIFO Data Buffer
                lastBits = self.readRFID(self.ControlReg) & 0x07#get the number of valid bits in the last recived byte from the control reg (stored in bits 0-2)
                if lastBits != 0:#Check if last bit is at end of byte
                    backLen = (n - 1) * 8 + lastBits#set bit length if last bit is not at the end of a byte
                else:
                    backLen = n * 8#set bit length if last bit is at the end of a byte

                if n == 0:#if byte length is 0 then set to 1
                    n = 1
                if n > self.MAX_LEN:#if byte legth is greater than Max length used then set byte length to data used
                    n = self.MAX_LEN

                for i in range(n):#read the correct number of bytes from the FIFO Data Buffer 
                    backData.append(self.readRFID(self.FIFODataReg))#put data from FIFO Data Buffer in backData
            else:
                status = self.STATUS_ERROR

        return (status, backData, backLen)
    
    #Request command for PICC. Invites PICCs in state IDLE to go to READY and prepare for anticollision or selection. The PICC then responds back to the RFID reader so the RFID reader knows there is a PICC within range.
    def requestPICC(self):
        status = None #status variable
        backBits = None #amount of bits of data from PICC
        Command= [] #for holding command
        Command.append(self.COMMAND_PICC_REQA)#Add Request Command to invite PICC in idle state to move to ready state 

        self.writeRFID(self.BitFramingReg, 0x07)#Set TxLastBits[2:0] to not transmit last byte
        
        (status, backData, backBits) = self.sendToPICC(Command)#Send Request Command to PICCs
       
        if ((status != self.STATUS_OK) | (backBits != 0x10)):#Check for Error
            status = self.STATUS_ERROR
        return (status, backBits)
        
    


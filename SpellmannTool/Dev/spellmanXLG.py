# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:11:24 2019

@author: justRandom

Generate CSUM according to spellman documents
"""
import serial
import time




class xlg():

    def __init__(self):
        print()
        
    def __del__(self):
        self.xlg.close()
        
    def connectPort(self, port):
        self.xlg = serial.Serial('COM'+str(port), baudrate=9600, timeout=1)

    #Calculate checksum
    def generateCSUM(self, arg):
        buf = 0
        for i in range(len(arg)):
            buf += ord(arg[i])
        buf = buf % 0x100
        check = str(format(buf, 'x'))
        if(len(check) == 1):
            check = '0'+check
        return(check)

    # Set XLG
    # Voltage [V]
    # Crurrent [mA]
    def setXLG(self, voltage, current, HV_ON):
        if(voltage >= 0 and voltage <= 60000):
            vHex = "%0.3X" % int(4095 * (voltage/60000))
            print(vHex)
        else:
            print('ERROR: voltage out of range: 0-60000[V]')
            return
        if(current >= 0 and current <= 15):
            cHex = "%0.3X" % int(4095 * (current/15))     
        else:
            print('ERROR: current out of range: 0-15[mA]')
            return
        #Activate HV Output
        if(HV_ON == True):
            status = str(0b0001)
        #Deactivate HV output
        if(HV_ON == False):
            status = str(0b0100)
        command = ('S'+vHex+cHex+'000000'+status)
        checksum = self.generateCSUM(command)
        commandString = ('\1'+command+checksum+'\r')
        self.xlg.write(commandString.encode())
        return()
  
    #Reads the status of the XLG
    #Returns lexicon
    def getXLG(self):
        #Status Lexicon
        xlgStatus = {
                "voltage":              0,
                "current":              0,
                "arcError":             False,
                "regulationError":      False,
                "tempError":            False,
                "InterlockError":       False,
                "coolingError":         False,
                "overCurrent":          False,
                "overVoltage":          False,
                "remote":               False           
                }
        self.xlg.read_all()
        request = ('\1'+'Q51\r').encode()
        self.xlg.write(request)
        answer = self.xlg.readline().decode()
        #Read measured current and voltage    
        xlgStatus["voltage"] = int(int(answer[1:4],16) / 1023 * 60000)
        xlgStatus["current"] = "%.4f" % (int(answer[4:7],16) / 1023 * 15)
        #Get Status bits
        byte11 = int(answer[11])
        byte12 = int(answer[12])
        byte13 = int(answer[13])
        if(byte11 & 0b0001):
            xlgStatus["arcError"]=True 
        if(byte11 & 0b0010):
            xlgStatus["regulationError"]=True
        if(byte11 & 0b0100):
            xlgStatus["tempError"]=True
        if(byte11 & 0b1000):
            xlgStatus["interlockError"]=True      
        if(byte12 & 0b0001):
            xlgStatus["coolingError"]=True
        if(byte12 & 0b0010):
            xlgStatus["overCurrent"]=True        
        if(byte12 & 0b1000):
            xlgStatus["overVoltage"]=True        
        if(byte13 & 0b0001):
            xlgStatus["remote"]=True
        #return lexicon
        return(xlgStatus)
        


    
    
    
    
    
    
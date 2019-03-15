# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:11:24 2019

@author: justRandom

Generate CSUM according to spellman documents
"""
import serial
import time

#Enable Disable Simulation of Instrument
sim = True

#Set xlg serial
if sim == False:
    xlg = serial.Serial('COM17', baudrate=9600, timeout=1)

#Calculate checksum
def generateCSUM(arg):
    buf = 0
    for i in range(len(arg)):
        buf += ord(arg[i])
    buf = buf % 0x100
    check = str(format(buf, 'x'))
    if(len(check) == 1):
        check = '0'+check
    return(check)

# Set XLG
def setXLG(voltage, current, HV_ON):
    if(voltage >= 0 and voltage <= 60000):
        vHex = "%0.3X" % int(4095 * (voltage/60000))
    else:
        print('ERROR: voltage out of range: 0-60000[V]')
        return
    if(current >= 0 and current <= 0.015):
        cHex = "%0.3X" % int(4095 * (current/0.015))     
    else:
        print('ERROR: current out of range: 0-0.015[A]')
        return
    #Activate HV Output
    if(HV_ON == True):
        status = str(0b0001)
    #Deactivate HV output
    if(HV_ON == False):
        status = str(0b0100)
    command = ('S'+vHex+cHex+'000000'+status)
    checksum = generateCSUM(command)
    commandString = ('\1'+command+checksum+'\r')
    if sim == False:
        xlg.write(commandString.encode())
    if sim == True:
        print(commandString)
        print(commandString.encode())
    return()
  
#Reads the status of the XLG
#Returns lexicon
def getXLG(debug=''):
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
    #Get data and check checksum 10 times before exiting
    dataValid = False
    for i in range(10):
        time.sleep(.5)
        if sim == False:
            xlg.flushInput()
            time.sleep(.5)
            request = ('\1'+'Q51\r').encode()
            xlg.write(request)
            answer = xlg.readline().decode()
        if sim == True:
            answer = debug
        if(1):#int(generateCSUM(answer[1:13])) is int(answer[13:])):
            dataValid = True
            break
    #If no valid package received then break
    if(dataValid is not True):
        print("ERROR: No valid data packet received...")
        return()
    #Read measured current and voltage    
    xlgStatus["voltage"] = int(int(answer[1:4],16) / 1023 * 60000)
    xlgStatus["current"] = (int(answer[4:7],16) / 1023 * 0.015)
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


setXLG(33000, 0.00375, True)



'''
setXLG(56000,0.0002,True)  
while(True):
    time.sleep(1)
    print(getXLG())
    if(input() == 'x'):
        break
    
setXLG(0,0,False)  

xlg.close()
'''

    
    
    
    
    
    
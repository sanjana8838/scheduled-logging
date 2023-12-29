#Import Libraries
import pandas as pd
from pymodbus.client import ModbusTcpClient
import datetime
import time
import logging
import schedule
import ctypes

from apscheduler.schedulers.background import BackgroundScheduler, BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime

#Global variable definition
global voltage1
global voltage2
global current2
global logger1

#Payload definition
ploads = {
    "TIMESTAMP":0,
    "VOLTAGE1" :0,
    "CURRENT1" :0,
    "BUS_CURRENT" :0,
    "TEMPERATURE1":0,
    "OCV1":0,
    "SOC":0
}

df = pd.DataFrame(ploads, index=[0])

#Modbus TCP client Connection
def ModbusConnect(ip="192.168.0.25", port=1502):
    global client 
    client = ModbusTcpClient(ip, port=port)
    connect = client.connect()
    
ModbusConnect()

#Handling negative values for 16 bit numbers
def NegativeValue(n):
    num = int((int(n[0])))
    num = num & 0xFFFF
    num = ctypes.c_int16(num).value
    return num

#Modbus Holding register read
def ReadRegister():
    timestamp1 = int(time.time())

    timestamp2 = str(datetime.now())
    ploads['TIMESTAMP'] = timestamp2

    voltage1 = client.read_holding_registers(53, 1, unit=1).registers
    ploads['VOLTAGE1'] = (int(voltage1[0]))/100

    current1 = client.read_holding_registers(52, 1, unit=1).registers
    current1 = NegativeValue(current1)
    ploads['CURRENT1'] = (int(current1))/100

    current2 = client.read_holding_registers(56, 1, unit=1).registers
    current2 = NegativeValue(current2)
    ploads['BUS_CURRENT'] = (int(current2))/100
    
    ocv1 = client.read_holding_registers(44, 1, unit=1).registers
    ploads['OCV1'] = (int(ocv1[0]))/1000
    
    temp1 = client.read_holding_registers(41, 1, unit=1).registers
    ploads['TEMPERATURE1'] = (int(temp1[0]))/100
    
    soc = client.read_holding_registers(66, 1, unit=1).registers
    ploads['SOC'] = (int(soc[0]))/100

    global df

    df.loc[-1] = [ploads['TIMESTAMP'],  ploads['VOLTAGE1'], ploads['CURRENT1'], ploads['BUS_CURRENT'], ploads['TEMPERATURE1'], ploads['OCV1'],  ploads['SOC']]  # adding a row
    df.index = df.index + 1  # shifting index
    df = df.sort_index(ascending=False)  # sorting by index

    save_csv()
    
def save_csv():
    df.to_csv("Logged_data.csv")
    
if __name__== "__main__":
    executors = {'default': ThreadPoolExecutor(20)}
    scheduler = BackgroundScheduler ( executors = executors, job_defaults={'max_instances':2})

    #Interval definition
    intervalTrigger1= IntervalTrigger(seconds=1) 
    #Job to do
    scheduler.add_job(ReadRegister, intervalTrigger1)
    scheduler.start()
    

from machine import I2C, Pin, ADC, UART
from lis3dh import LIS3DH, LIS3DH_I2C, RANGE_4_G, DATARATE_1_HZ
from serial import Serial
import time
import os
import sys

if sys.platform == 'esp32': # ESP32
  scl_pin = Pin(22, pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
  sda_pin = Pin(21, pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
  ADC.width(ADC.WIDTH_12BIT)
  thermistor = ADC(Pin(34))
  thermistor.atten(ADC.ATTN_11DB) # Full range: 3.3v
else:
  print('Incompatible board detected, please connect ESP32')
  
i2c = I2C(-1, scl=scl_pin, sda=sda_pin)
accelerometer = LIS3DH_I2C(i2c, int1=None)

LIS3DH.range = RANGE_4_G # Setting range to 4G
LIS3DH.datarate = DATARATE_1_HZ # Setting data rate to 1 Hz

# Setting up communication
uart_id = 0x01
modbus_obj = Serial(uart_id)

while True:
  # Print X,Y,Z acceleration values in m/s^2
  x, y, z = [value for value in accelerometer.acceleration]
  print(x,y,z)

  # Read value of thermistor
  temp = thermistor.read() / (2**12)
  temp *= 100
  print(temp)
  print()
  
  time.sleep(1)

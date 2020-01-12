from machine import I2C, Pin, ADC, UART
from lis3dh import LIS3DH, LIS3DH_I2C, RANGE_2_G, DATARATE_1_HZ
from serial import Serial
import time
import os
import sys
import math

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

LIS3DH.range = RANGE_2_G # Setting range to 2G
LIS3DH.datarate = DATARATE_1_HZ # Setting data rate to 1 Hz

# Setting up communication
uart_id = 0x01
modbus_obj = Serial(uart_id)

while True:
  # Print X,Y,Z acceleration values in m/s^2
  x, y, z = [value for value in accelerometer.acceleration]

  xRounded = round(x, 2)
  yRounded = round(y, 2)
  zRounded = round(z, 2)
  print(xRounded, yRounded, zRounded)
  
  #print()
  """
  # Read value of thermistor
  print(thermistor.read())
  inverseADC = 4095 - thermistor.read()
  print(inverseADC)
  temp = inverseADC / (2**12 - 1)
  temp -= 0.5
  temp *= 100
  #temp *= 165
  #temp -= 40
  temp = round(temp, 2)
  print(temp)
  print()
  """
  voltage = (thermistor.read() / 4095) * 3.3
  temp = (voltage - 0.5) * 100
  print(temp)
  
  print()
  
  # Writing coil
  slave_addr=0x0A
  output_address=0x00
  output_value=0xFF00

  #return_flag = modbus_obj.write_single_coil(slave_addr, output_address, output_value)
  #output_flag = 'Success' if return_flag else 'Failure'
  #print('Writing single coil status: ' + output_flag)
  #print()
  
  time.sleep(1)





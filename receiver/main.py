from machine import I2C, Pin, ADC, UART
from lis3dh import LIS3DH, LIS3DH_I2C, RANGE_2_G, DATARATE_1_HZ
from serial import Serial
import time
import os
import sys
import math
import machine

if sys.platform == 'esp32': # ESP32
  scl_pin = Pin(22, pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
  sda_pin = Pin(21, pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
  ADC.width(ADC.WIDTH_12BIT)
  thermistor = ADC(Pin(34))
  thermistor.atten(ADC.ATTN_11DB) # Full range: 3.3v
  #uart = UART(uart_id, baudrate=9600, bits=8, parity=None, stop=1)
  uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1)
else:
  print('Incompatible board detected, please connect ESP32')
  
i2c = I2C(-1, scl=scl_pin, sda=sda_pin)
accelerometer = LIS3DH_I2C(i2c, int1=None)

LIS3DH.range = RANGE_2_G # Setting range to 2G
LIS3DH.datarate = DATARATE_1_HZ # Setting data rate to 1 Hz

# Setting up communication
#uart_id = 0x01
#modbus_obj = Serial(uart_id)

while True:
  # Print X,Y,Z acceleration values in m/s^2
  x, y, z = [value for value in accelerometer.acceleration]

  xRounded = round(x, 2)
  yRounded = round(y, 2)
  zRounded = round(z, 2)
  print(xRounded, yRounded, zRounded)
  
  # Thermistor (Two approaches, need further testings as code fluctuates
  voltage = (thermistor.read() / 4095) * 3.3
  temp = (voltage - 0.5) * 100
  tempRounded = round(temp, 2)
  print(tempRounded)
  
  thermistorTest = thermistor.read() / 4095
  thermistorTest *= 100
  thermistorTest = round(thermistorTest, 2)
  print(thermistorTest)
  
  print(uart.read())
  
  print()
  
  time.sleep(1)
  #machine.deepsleep(1000) # Deep sleep mode for 1 s, may change to gpio pin e.g. rx
  
  """
  # Modbus functions
  ######################### READ COILS #########################
  #slave_addr=0x0A
  #starting_address=0x00
  #coil_quantity=100

  #coil_status = modbus_obj.read_coils(slave_addr, starting_address, coil_quantity)
  #print('Coil status: ' + ' '.join('{:d}'.format(x) for x in coil_status))

  ###################### READ DISCRETE INPUTS ##################
  #slave_addr=0x0A
  #starting_address=0x0
  #input_quantity=100

  #input_status = modbus_obj.read_discrete_inputs(slave_addr, starting_address, input_quantity)
  #print('Input status: ' + ' '.join('{:d}'.format(x) for x in input_status))

  ###################### READ HOLDING REGISTERS ##################
  #slave_addr=0x0A
  #starting_address=0x00
  #register_quantity=100
  #signed=True

  #register_value = modbus_obj.read_holding_registers(slave_addr, starting_address, register_quantity, signed)
  #print('Holding register value: ' + ' '.join('{:d}'.format(x) for x in register_value))

  ###################### READ INPUT REGISTERS ##################
  #slave_addr=0x0A
  #starting_address=0x00
  #register_quantity=100
  #signed=True

  #register_value = modbus_obj.read_input_registers(slave_addr, starting_address, register_quantity, signed)
  #print('Input register value: ' + ' '.join('{:d}'.format(x) for x in register_value))

  ###################### WRITE SINGLE COIL ##################
  #slave_addr=0x0A
  #output_address=0x00
  #output_value=0xFF00

  #return_flag = modbus_obj.write_single_coil(slave_addr, output_address, output_value)
  #output_flag = 'Success' if return_flag else 'Failure'
  #print('Writing single coil status: ' + output_flag)

  ###################### WRITE SINGLE REGISTER ##################
  #slave_addr=0x0A
  #register_address=0x01
  #register_value=-32768
  #signed=True

  #return_flag = modbus_obj.write_single_register(slave_addr, register_address, register_value, signed)
  #output_flag = 'Success' if return_flag else 'Failure'
  #print('Writing single coil status: ' + output_flag)

  ###################### WRITE MULIPLE COILS ##################
  #slave_addr=0x0A
  #starting_address=0x00
  #output_values=[1,1,1,0,0,1,1,1,0,0,1,1,1]

  #return_flag = modbus_obj.write_multiple_coils(slave_addr, starting_address, output_values)
  #output_flag = 'Success' if return_flag else 'Failure'
  #print('Writing multiple coil status: ' + output_flag)

  ###################### WRITE MULIPLE REGISTERS ##################
  #slave_addr=0x0A
  #register_address=0x01
  #register_values=[2, -4, 6, -256, 1024]
  #signed=True

  #return_flag = modbus_obj.write_multiple_registers(slave_addr, register_address, register_values, signed)
  #output_flag = 'Success' if return_flag else 'Failure'
  #print('Writing multiple register status: ' + output_flag)
  """










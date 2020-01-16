# Author: Kevin Tangfrom machine import Pin, I2C, SPI, UARTfrom ds3231_port import DS3231from pyb import RTCimport utimeimport timeimport sysimport os# mode and pull are specified in case pullups are absent.if sys.platform == 'pyboard':  # Pin connections  scl_pin = Pin('X9', pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)  sda_pin = Pin('X10', pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)  tx_enable = Pin('X20', mode=Pin.OUT)    # RTC initialisation  i2c = I2C(-1, scl=scl_pin, sda=sda_pin)   ds3231 = DS3231(i2c)    # UART initialisation  uart = UART(6, 9600) # Pin: Y1 and Y2  uart.init(9600, bits=8, parity=None, stop=1, timeout=0)  else:   print('Incompatible system detected, please connect a pyboard')  # Date initialisationrtc = RTC()timeCheck = ds3231.get_time() # Gets current timertc.datetime((timeCheck[0], timeCheck[1], timeCheck[2], timeCheck[6], timeCheck[3], timeCheck[4], timeCheck[5], 0)) # Syncs RTC clock to local time"""# Sets up RTC clock, uncomment to manually set the clock (NOTE: DAY OF WEEK AND TIME ZONE IS NOT WORKING)rtc.datetime((2020, 1, 13, 1, 11, 32, 10, 0))  # Comment out if already programmedds3231.save_time()# RTC Format: YY, MM, DD, Day of week (Mon = 1), hh, mm, ss, time zone# Example: 16/12/2019 @ Monday 16:13:00# = rtc.datetime((2019, 12, 16, 1, 16, 13, 0, 0))"""# Checks to see if the csv file is empty, then writes the file if it is emptytry:  with open("/sd/accelerometer1.csv") as fileEmptyTest:    emptyTest = fileEmptyTest.read(1)    if not emptyTest:      print('writing headers')      log_header1 = open("/sd/accelerometer1.csv", "a")      log_header1.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header1.close()      log_header2 = open("/sd/accelerometer2.csv", "a")      log_header2.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header2.close()      log_header3 = open("/sd/accelerometer3.csv", "a")      log_header3.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header3.close()      log_header4 = open("/sd/accelerometer4.csv", "a")      log_header4.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header4.close()      log_header5 = open("/sd/accelerometer5.csv", "a")      log_header5.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header5.close()      log_header6 = open("/sd/accelerometer6.csv", "a")      log_header6.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header6.close()      log_header7 = open("/sd/accelerometer7.csv", "a")      log_header7.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header7.close()      log_header8 = open("/sd/accelerometer8.csv", "a")      log_header8.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header8.close()      log_header9 = open("/sd/accelerometer9.csv", "a")      log_header9.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header9.close()      log_header10 = open("/sd/accelerometer10.csv", "a")      log_header10.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")      log_header10.close()    else:      print('csv file is not empty')except OSError: # File does not exist, thus giving the error. Make the files with the headers  print('writing headers')  log_header1 = open("/sd/accelerometer1.csv", "a")  log_header1.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header1.close()  log_header2 = open("/sd/accelerometer2.csv", "a")  log_header2.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header2.close()  log_header3 = open("/sd/accelerometer3.csv", "a")  log_header3.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header3.close()  log_header4 = open("/sd/accelerometer4.csv", "a")  log_header4.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header4.close()  log_header5 = open("/sd/accelerometer5.csv", "a")  log_header5.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header5.close()  log_header6 = open("/sd/accelerometer6.csv", "a")  log_header6.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header6.close()  log_header7 = open("/sd/accelerometer7.csv", "a")  log_header7.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header7.close()  log_header8 = open("/sd/accelerometer8.csv", "a")  log_header8.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header8.close()  log_header9 = open("/sd/accelerometer9.csv", "a")  log_header9.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header9.close()  log_header10 = open("/sd/accelerometer10.csv", "a")  log_header10.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")  log_header10.close()# Retrieves datedef getDate():  return str(rtc.datetime()[2]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[0])# Retrieves timedef getTime():  return str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])# Low power delaydef secondTimer():  if pyb.Pin.board.USB_VBUS.value() == 1: #pyb.stop() will kill USB connection to pyboard    time.sleep(0.5)  else:    rtc.wakeup(500) # Allows the Pyboard to wake up every second    pyb.stop() # Pyboard will enter low power mode to conserve battery life    rtc.wakeup(None)  while True:  tx_enable.value(0)  print(getDate()) # Date  print(getTime()) # Time  test = uart.read()  dataString = str(test)[2:-1]  splitString = dataString.split(",")  print(splitString)    # Writing to files  # Format: ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature  if(splitString[0] == '0'):    log_header1 = open("/sd/accelerometer1.csv", "a")    log_header1.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header1.close()  elif(splitString[0] == '1'):    log_header2 = open("/sd/accelerometer2.csv", "a")    log_header2.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()  elif(splitString[0] == '2'):    log_header3 = open("/sd/accelerometer3.csv", "a")    log_header3.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    log_header3.close()  elif(splitString[0] == '3'):    log_header4 = open("/sd/accelerometer4.csv", "a")    log_header4.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header4.close()  elif(splitString[0] == '4'):    log_header5 = open("/sd/accelerometer5.csv", "a")    log_header5.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header5.close()  elif(splitString[0] == '5'):    log_header6 = open("/sd/accelerometer6.csv", "a")    log_header6.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header6.close()  elif(splitString[0] == '6'):    log_header7 = open("/sd/accelerometer7.csv", "a")    log_header7.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header7.close()  elif(splitString[0] == '7'):    log_header8 = open("/sd/accelerometer8.csv", "a")    log_header8.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header8.close()  elif(splitString[0] == '8'):    log_header9 = open("/sd/accelerometer9.csv", "a")    log_header9.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header9.close()  elif(splitString[0] == '9'):    log_header10 = open("/sd/accelerometer10.csv", "a")    log_header10.write(splitString[0] + ", " + getDate() + ", " + getTime() + ", " + splitString[1] + ", " + splitString[2] + ", " +    splitString[3] + ", " + splitString[4] + " \n")    pyb.LED(4).on()    log_header10.close()  else:    print('No data to write')    secondTimer()  pyb.LED(4).off()  secondTimer()
# Datalogger code for Cawthron Institute's mussel farm accelerometer chain# Author: Kevin Tangfrom machine import Pin, I2C, SPI, UART, WDTfrom ds3231_port import DS3231from pyb import RTCimport utimeimport timeimport sysimport osglobal startglobal finish# Modesglobal DATA_RATE_1HZglobal DATA_RATE_2HZglobal MODEDATA_RATE_1HZ = 'one'DATA_RATE_2HZ = 'two'MODE = DATA_RATE_2HZ # Choose modes here (DATA_RATE_1HZ or DATA_RATE_2HZ)# Enable Watchdog timer when batteries are plugged in.if pyb.Pin.board.USB_VBUS.value() == 0:  wdt = WDT(timeout=10000) # enable with a timeout of 10 secondsif sys.platform == 'pyboard':  # Pin connections  tx_enable = Pin('X20', mode=Pin.OUT)    # RTC initialisation  i2c = I2C(1) # Pins X9 and X10  ds3231 = DS3231(i2c)    # UART initialisation  uart = UART(4, 115200) # Pins X1 and X2  uart.init(115200, bits=8, parity=None, stop=1, timeout=1000) # Non-blocking UART  else:   print('Incompatible system detected, please connect a pyboard')  # Date initialisationrtc = RTC()timeCheck = ds3231.get_time() # Gets current timertc.datetime((timeCheck[0], timeCheck[1], timeCheck[2], timeCheck[6], timeCheck[3], timeCheck[4], timeCheck[5], 0)) # Syncs RTC clock to local time"""# Sets up RTC clock, uncomment to manually set the clock (NOTE: DAY OF WEEK AND TIME ZONE IS NOT WORKING)rtc.datetime((2020, 1, 27, 1, 12, 11, 30, 0))  # Comment out if already programmedds3231.save_time()# RTC Format: YY, MM, DD, Day of week (Mon = 1), hh, mm, ss, time zone# Example: 16/12/2019 @ Monday 16:13:00# = rtc.datetime((2019, 12, 16, 1, 16, 13, 0, 0))"""# Checks to see if the csv file is empty, then writes the file if it is emptyfor i in range(10):  string = "/sd/accelerometer" + str(i) + ".csv"  try:    with open(string) as fileEmptyTest:      emptyTest = fileEmptyTest.read(1)      if not emptyTest:        log_header = open(string, "a")        log_header.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")        log_header.close()   except OSError: # File does not exist, make the files and headers    log_header = open(string, "a")    log_header.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")    log_header.close() # Retrieves datedef getDate():  return str(rtc.datetime()[2]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[0])# Retrieves timedef getTime():  return str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])# Sleep timerdef rest():  if MODE == DATA_RATE_1HZ:    if(pyb.Pin.board.USB_VBUS.value() == 1):      time.sleep(1)    else:      rtc.wakeup(1000 - finish)      pyb.stop()      rtc.wakeup(None)  else:    if(pyb.Pin.board.USB_VBUS.value() == 1):      time.sleep(10)    else:      rtc.wakeup(500)      pyb.stop()      rtc.wakeup(None)  # Reading UART value and converting to stringdef uartProcess():  test = uart.read()  dataString = str(test)[2:-4]  dataString = dataString.split('...')  splitString = [i.split(',') for i in dataString]  return splitString# Sends mode information to receiverdef modeSelection():  if MODE == DATA_RATE_1HZ:    uart.write("uno")  else:    uart.write("dos")# Remove WDT when USB is plugged indef wdtCheck():  if(pyb.Pin.board.USB_VBUS.value() == 0):    wdt.feed() # Resets receiver data buffers and respective sleep values based on mode selection on first starttx_enable.value(1)uart.write(MODE)tx_enable.value(0)while True:  wdtCheck()  print(getDate()) # Date  print(getTime()) # Time    tx_enable.value(1)  modeSelection()  uart.write('0')  tx_enable.value(0)  splitString = uartProcess()  print(splitString[0][0])  if(splitString[0][0] == '0'):    print('ok')    log_header0 = open("/sd/accelerometer0.csv", "a")    for i in range(len(splitString)):      log_header0.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header0.close()    pyb.LED(4).on()      tx_enable.value(1)  modeSelection()  uart.write('1')  tx_enable.value(0)  splitString = uartProcess()  print(splitString[0][0])  if(splitString[0][0] == '1'):    print('boomer')    log_header1 = open("/sd/accelerometer1.csv", "a")    for i in range(len(splitString)):      log_header1.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header1.close()    pyb.LED(3).on()      tx_enable.value(1)  modeSelection()  uart.write('2')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '2'):    log_header2 = open("/sd/accelerometer2.csv", "a")    for i in range(len(splitString)):      log_header2.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header2.close()    pyb.LED(4).on()      tx_enable.value(1)  modeSelection()  uart.write('3')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '3'):    log_header3 = open("/sd/accelerometer3.csv", "a")    for i in range(len(splitString)):      log_header3.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header3.close()    pyb.LED(4).on()      tx_enable.value(1)  modeSelection()  uart.write('4')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '0'):    log_header4 = open("/sd/accelerometer4.csv", "a")    for i in range(len(splitString)):      log_header4.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header4.close()    pyb.LED(4).on()      tx_enable.value(1)  modeSelection()  uart.write('5')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '5'):    log_header0 = open("/sd/accelerometer5.csv", "a")    for i in range(len(splitString)):      log_header5.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header5.close()    pyb.LED(4).on()    tx_enable.value(1)  modeSelection()  uart.write('6')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '6'):    log_header6 = open("/sd/accelerometer6.csv", "a")    for i in range(len(splitString)):      log_header6.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header6.close()    pyb.LED(4).on()      tx_enable.value(1)  modeSelection()  uart.write('7')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '7'):    log_header7 = open("/sd/accelerometer7.csv", "a")    for i in range(len(splitString)):      log_header7.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header7.close()    pyb.LED(4).on()    tx_enable.value(1)  modeSelection()  uart.write('8')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '8'):    log_header8 = open("/sd/accelerometer8.csv", "a")    for i in range(len(splitString)):      log_header8.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header8.close()    pyb.LED(4).on()    tx_enable.value(1)  modeSelection()  uart.write('9')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '9'):    log_header9 = open("/sd/accelerometer9.csv", "a")    for i in range(len(splitString)):      log_header9.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header9.close()    pyb.LED(4).on()    print()  pyb.LED(3).off()  pyb.LED(4).off()    rest()
# Datalogger code for Cawthron Institute's mussel farm accelerometer chain# Author: Kevin Tang"""DEFAULT SETTINGSMODE = DATA_RATE_1HZBAUD RATE: 9600UART DATA FRAME: bits=8, parity=None, stop=1, timeout=1000WDT TIMEOUT: 3000ms1 HZ SLEEP: 30s2 HZ SLEEP: 10s"""from machine import Pin, I2C, SPI, UART, WDTfrom ds3231_port import DS3231from pyb import RTCimport utimeimport timeimport sysimport os# Timeout valuesglobal SLEEP_1HZglobal SLEEP_2HZSLEEP_1HZ = 30SLEEP_2HZ = 10# Modesglobal DATA_RATE_1HZglobal DATA_RATE_2HZglobal MODEDATA_RATE_1HZ = 'one'DATA_RATE_2HZ = 'two'MODE = DATA_RATE_1HZ # Choose modes here (DATA_RATE_1HZ or DATA_RATE_2HZ)# Enable Watchdog timer when batteries are plugged in.global TIMEOUT_VALUETIMEOUT_VALUE = 3000if pyb.Pin.board.USB_VBUS.value() == 0:  wdt = WDT(timeout = TIMEOUT_VALUE) # enable watchdog timerif sys.platform == 'pyboard':  # Pin connections  tx_enable = Pin('X20', mode=Pin.OUT)    # RTC initialisation  i2c = I2C(1) # Pins X9 and X10  ds3231 = DS3231(i2c)    # UART initialisation  uart = UART(4, 115200) # Pins X1 and X2  uart.init(115200, bits=8, parity=None, stop=1, timeout=1000) # Blocking UART of 1 second  else:   print('Incompatible system detected, please connect a pyboard')  # Date initialisationrtc = RTC()timeCheck = ds3231.get_time() # Gets current timertc.datetime((timeCheck[0], timeCheck[1], timeCheck[2], timeCheck[6], timeCheck[3], timeCheck[4], timeCheck[5], 0)) # Syncs RTC clock to local time"""# Sets up RTC, uncomment to manually set the clock (NOTE: DAY OF WEEK AND TIME ZONE IS NOT WORKING)rtc.datetime((2020, 2, 11, 2, 16, 7, 40, 0))  # Comment out if already programmedds3231.save_time()# RTC Format: YY, MM, DD, Day of week (Mon = 1), hh, mm, ss, time zone# Example: 16/12/2019 @ Monday 16:13:00# = rtc.datetime((2019, 12, 16, 1, 16, 13, 0, 0))"""# Checks to see if the csv file is empty, then writes the file if it is emptyfor i in range(10):  string = "/sd/accelerometer" + str(i) + ".csv"  try:    with open(string) as fileEmptyTest:      emptyTest = fileEmptyTest.read(1)      if not emptyTest:        log_header = open(string, "a")        log_header.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")        log_header.close()   except OSError: # File does not exist, make the files and headers    log_header = open(string, "a")    log_header.write("ID, Date, Time, X Acceleration, Y Acceleration, Z Acceleration, Temperature \n")    log_header.close() # Retrieves datedef getDate():  return str(rtc.datetime()[2]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[0])# Retrieves timedef getTime():  return str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])# Sleep timerdef rest():  if MODE == DATA_RATE_1HZ:    for i in range(SLEEP_1HZ - 1):      if(pyb.Pin.board.USB_VBUS.value() == 1):        time.sleep(1)      else:        wdt.feed()        rtc.wakeup(1000)        pyb.stop()        rtc.wakeup(None)  else:    for i in range(SLEEP_2HZ - 1):      wdt.feed()      if(pyb.Pin.board.USB_VBUS.value() == 1):        time.sleep(1)      else:        wdt.feed()        rtc.wakeup(1000)        pyb.stop()        rtc.wakeup(None)  # Reading UART value and converting to stringdef uartProcess():  test = uart.read()  dataString = str(test)[2:-4]  dataString = dataString.split('...')  splitString = [i.split(',') for i in dataString]  return splitString# Sends mode information to receiverdef modeSelection():  if MODE == DATA_RATE_1HZ:    uart.write("uno")  else:    uart.write("dos")# Remove WDT when USB is plugged indef wdtCheck():  if(pyb.Pin.board.USB_VBUS.value() == 0):    wdt.feed()   # Checks if the last character is a digit and force reset if it isn't (garbage value check)global lastChardef charCheck():  try:    testing = [i for i in lastChar if i.isdigit()]    if testing == []:      print("Non digit detected. Forcing reset")      wdt = WDT(timeout = 1) # Force watchdog timer  except:    print('Exception Error. Forcing reset')    wdt = WDT(timeout = 1) # Force watchdog timer  # Resets receiver data buffers and respective sleep values based on mode selection on first starttx_enable.value(1)uart.write(MODE)tx_enable.value(0)while True:  wdtCheck()  print(getDate()) # Date  print(getTime()) # Time    # Print mode  if MODE == DATA_RATE_1HZ:    print("Mode: 1 Hz")  else:    print("Mode: 2 Hz")    tx_enable.value(1)  modeSelection()  uart.write('0')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '0'):    log_header0 = open("/sd/accelerometer0.csv", "a")    for i in range(len(splitString)):      log_header0.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header0.close()    print("Receiver 0 logged")    pyb.LED(1).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()    wdtCheck()  tx_enable.value(1)  modeSelection()  uart.write('1')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '1'):    log_header1 = open("/sd/accelerometer1.csv", "a")    for i in range(len(splitString)):      log_header1.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header1.close()    print("Receiver 1 logged")    pyb.LED(1).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()    wdtCheck()  tx_enable.value(1)  modeSelection()  uart.write('2')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '2'):    log_header2 = open("/sd/accelerometer2.csv", "a")    for i in range(len(splitString)):      log_header2.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header2.close()    print("Receiver 2 logged")    pyb.LED(2).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()     wdtCheck()   tx_enable.value(1)  modeSelection()  uart.write('3')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '3'):    log_header3 = open("/sd/accelerometer3.csv", "a")    for i in range(len(splitString)):      log_header3.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header3.close()    print("Receiver 3 logged")    pyb.LED(2).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()     wdtCheck()   tx_enable.value(1)  modeSelection()  uart.write('4')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '4'):    log_header4 = open("/sd/accelerometer4.csv", "a")    for i in range(len(splitString)):      log_header4.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header4.close()    print("Receiver 4 logged")    pyb.LED(2).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()      wdtCheck()  tx_enable.value(1)  modeSelection()  uart.write('5')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '5'):    log_header5 = open("/sd/accelerometer5.csv", "a")    for i in range(len(splitString)):      log_header5.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header5.close()    print("Receiver 5 logged")    pyb.LED(3).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()    wdtCheck()  tx_enable.value(1)  modeSelection()  uart.write('6')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '6'):    log_header6 = open("/sd/accelerometer6.csv", "a")    for i in range(len(splitString)):      log_header6.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header6.close()    print("Receiver 6 logged")    pyb.LED(3).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()     wdtCheck()   tx_enable.value(1)  modeSelection()  uart.write('7')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '7'):    log_header7 = open("/sd/accelerometer7.csv", "a")    for i in range(len(splitString)):      log_header7.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header7.close()    print("Receiver 7 logged")    pyb.LED(3).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()    wdtCheck()  tx_enable.value(1)  modeSelection()  uart.write('8')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '8'):    log_header8 = open("/sd/accelerometer8.csv", "a")    for i in range(len(splitString)):      log_header8.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header8.close()    print("Receiver 8 logged")    pyb.LED(4).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()    wdtCheck()  tx_enable.value(1)  modeSelection()  uart.write('9')  tx_enable.value(0)  splitString = uartProcess()  if(splitString[0][0] == '9'):    log_header9 = open("/sd/accelerometer9.csv", "a")    for i in range(len(splitString)):      log_header9.write(splitString[i][0] + ", " + splitString[i][1] + ", " + splitString[i][2] + ", " + splitString[i][3] + ", " \      + splitString[i][4] + ", " + splitString[i][5] + ", " + splitString[i][6] + " \n")    log_header9.close()    print("Receiver 9 logged")    pyb.LED(4).on()    lastTemp = splitString[-1][-1]    lastChar = list(lastTemp[-1])    charCheck()    print()  pyb.LED(1).off()  pyb.LED(2).off()  pyb.LED(3).off()  pyb.LED(4).off()    wdtCheck()  rest()
# Cawthron Accelerometer Chain

## Author: Kevin Tang

### I wrote this code for Cawthron Institute during my internship, it is to measure the acceleration at 10 different points of the mussel farm rope and to log the data on a single SD card.

The file has three folders: 

* `receiver` for the receiver component measuring the acceleration and the temperature
* `datalogger` for requesting the data from the receiver and to log them on the SD card
* `PCB` containing the PCB files

## Code Setup

* `git clone` or download the code as a zip file

* Download uPycraft IDE or simply use a text editor such as Notepad++

* Copy respective files (main.py + boot.py + libraries) to SD card

**NOTE: If the SD card is larger than 32GB, use GUIFormat to format SD card to FAT32**

### Datalogger

1. Choose datalogging mode in `MODE` to `MODE = DATA_RATE_1HZ` for 1 Hz or `MODE = DATA_RATE_2HZ` for 2 Hz

2. To set up RTC, uncomment section under date initialisation and follow formatting

3. Run the code to save the time

4. Comment out the RTC code section as before to stop it from re-initialising the time each time

5. Rerun the code

* The red LED will light up to signify receiver 0 and/or 1 information has been received

* The green LED will light up to signify receiver 2 and/or 3 and/or 4 information has been received

* The yellow LED will light up to signify receiver 5 and/or 6 and/or 7 information has been received

* The blue LED will light up to signify receiver 8 and/or 9 information has been received

### Receiver

1. Configure ID from 0-9 under `ID = _` **MAKE SURE EACH ID NUMBER IS DIFFERENT**

2. To set up RTC, uncomment section under date initialisation and follow formatting

3. Run the code to save the time

4. Comment out the RTC code section as before to stop it from re-initialising the time each time

5. Rerun the code

* The Green LED will flash to signify the receiver has transmitted to the datalogger 

## PCB

Components needed and links for 1 datalogger and 10 receivers:

* [11 x Pyboard](https://www.digikey.co.nz/products/en?mpart=DEV-14412&v=1568)

* [11 x 1N4148](https://nz.element14.com/diodes-inc/1n4148w-7-f/diode-switch-300ma-100v-sod123/dp/1776392?st=1N4148W-7-F)

* [11 x 47uF Electrolytic Capacitor](https://nz.element14.com/panasonic/eee1ca470sp/ae-capacitor-case-radial-can-smd/dp/9696946?st=47uF%20electrolytic%20smt)

* [11 x 100nF Capacitor](https://nz.element14.com/avx/08055c104jat2a/cap-0-1-f-50v-5-x7r-0805/dp/1740673?st=100nF%200805)

* [11 x DS3231M](https://www.digikey.co.nz/product-detail/en/maxim-integrated/DS3231MPMB1/DS3231MPMB1-ND/3661364)

* [11 x CR1025 Batteries](https://www.mrpositive.co.nz/panasonic-cr1025-3v-lithium-button-cell-battery)

* [11 x TTL to RS485 Converter](https://www.aliexpress.com/item/32668863095.html)

* [10 x LIS3DH](https://www.adafruit.com/product/2809)

* [10 x TMP36](https://www.digikey.co.nz/product-detail/en/analog-devices-inc/TMP36GT9Z/TMP36GT9Z-ND/820404)

* M3 Standoffs (Optional)

Wiring diagram is provided in the PCB folder (datalogger_schematic.PNG and receiver_schematic.PNG)

Make sure the terminal A connect with other terminal A and same for terminal B

## Ordering PCBs 

I have provided the zip files containing gerber files and NC drill files in the PCB folder (Datalogger_v3.zip and Receiver_v3.zip)
[JLCPCB](https://jlcpcb.com/) is recommended

Datalogger board size: 74mm x 73mm

Receiver board size: 74mm x 70mm

## Troubleshooting

* Sometimes the compiler will append code at the bottom of original code, make sure to delete it

* If all the LEDs are flashing in order (e.g. board is corrupted), hold the USR button then the RST button.
Let go of the USR button and let go of the RST button once the yellow+green LEDs light up to reset board to factory settings.
Recopy code to SD card

* If there are errors in the code, make sure to copy the whole code, 
press Ctrl+E to enter copy paste mode in the REPL/console, paste the code then press Ctrl+D to run the code and view the error

* The csv file cannot be viewed while the SD card is plugged into the Pyboard. A SD card reader is required to view the csv file

* The watchdog timer has been disabled if the pyboard has been powered by a USB to ensure ease of debugging.
Make sure to power the Pyboard with a battery if in use.
Otherwise, enable the watchdog timers

**If there are any issues with the code/components email me or open up an issue on GitHub**
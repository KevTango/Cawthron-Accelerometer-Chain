# Cawthron Accelerometer Chain

## Author: Kevin Tang

### I wrote this code for Cawthron Institute during my internship, it is to measure the acceleration at 10 different points of the mussel farm rope and to log the data on a single SD card.

The file has three folders: 

* `receiver` for the receiver component measuring the acceleration and the temperature
* `datalogger` for requesting the data from the receiver and to log them on the SD card
* `PCB` containing the PCB files

## Code Setup

* Download uPycraft IDE

* Copy respective files (main.py + boot.py + libraries) to SD card

**NOTE: If SD card is larger than 32GB, use GUIFormat to format SD card to FAT32**

### Datalogger

1. Choose datalogging mode in: `MODE` to `MODE = DATA_RATE_1HZ` for 1 Hz or `MODE = DATA_RATE_2HZ` for 2 Hz

2. To set up RTC, uncomment section under date initialisation and follow formatting

3. Run the code to save the time

4. Comment out the RTC code section as before to stop it from re-initialising the time each time

5. Rerun the code

### Receiver

1. Configure ID from 0-9 under `ID = _` **MAKE SURE EACH ID NUMBER IS DIFFERENT**

2. To set up RTC, uncomment section under date initialisation and follow formatting

3. Run the code to save the time

4. Comment out the RTC code section as before to stop it from re-initialising the time each time

5. Rerun the code

## PCB

## Troubleshooting
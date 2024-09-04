Mela MicroPython Examples
====================

This repo features examples for Mela board MicroPython library.

# Troubleshooting


## 00.Basics

__boot.py__  
Sample boot file which loads mela library and initialize object "plc" from Mela class. The examples in this repo require this object. 

__main.py__  
Turns on RAM info output in cycle.


## 01.Modbus RTU
Contains two directories for two Mela boards. Master and Slave boards are connected via 485 interface.

### Slave

__boot.py__  
Sample boot file which loads mela library and initialize object "plc" from Mela class. The examples in this repo require this object. 

__main.py__  
Initialises Modbus RTU slave at 485 interface and loads register definitions. In this example we use 3 input registers, which contains current datetime, free RAM and VFS percentage. Data in registers updates evary 1 second vith Timer callback function.

__config.json__  
Contains Modbus RTU slave configuration.


### Master

__boot.py__  
Sample boot file which loads mela library and initialize object "plc" from Mela class. The examples in this repo require this object. 

__main.py__  
Initialises Modbus RTU master  at 485 interface and start polling data from slave with 10 seconds interval.

__config.json__  
Contains Modbus RTU master configuration.
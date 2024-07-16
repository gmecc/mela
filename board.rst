General information about the MELA board
========================================

The ESP32 is a popular WiFi and Bluetooth enabled System-on-Chip (SoC) by Espressif Systems.

Multitude of boards
-------------------

There is a multitude of modules and boards from different sources which carry the ESP32 chip.
MicroPython tries to provide a generic port which would run on as many boards/modules as possible,
but there may be limitations. Espressif development boards are taken
as reference for the port (for example, testing is performed on them).
For any board you are using please make sure you have a datasheet,
schematics and other reference materials so you can look up any board-specific functions.

To make a generic ESP32 port and support as many boards as possible
the following design and implementation decision were made:

GPIO pin numbering is based on ESP32 chip numbering.
Please have the manual/pin diagram of your board at hand to find correspondence
between your board pins and actual ESP32 pins.

All pins are supported by MicroPython but not all are usable on any given board.
For example pins that are connected to external SPI flash should not be used,
and a board may only expose a certain selection of pins.

Technical specifications and SoC datasheets
-------------------------------------------
The datasheets and other reference material for ESP32 chip are available
from the vendor site: https://www.espressif.com/en/support/download/documents?keys=esp32 .

They are the primary reference for the chip technical specifications, capabilities,
operating modes, internal functioning, etc.

For your convenience, some of technical specifications are provided below:

**MELA F1**

- Architecture: Xtensa Dual-Core 32-bit LX7
- Processor: RISC-V Ultra Low Power Co-processor
- CPU frequency: up to 240MHz
- Internal FlashROM: 32MB
- External FlashROM: Octal SPI PSRAM 8MB
- WiFi: 2.4GHz Wifi - 802.11b/g/n, 3D High Gain Antenna
- RTC: DS1307 with a CR1220 coin cell battery
- ADC: 16-bit delta-sigma ADC ADS1115 up to 4 channels 860SPS [0-10V / 0-20mA]
- Digital Input: 6 Digital Isolated Input [0-24V]
- Didital Output: 10; 6 PWM - Digital Isolated Output OK [0-24V 2A]; 4 Relay [250V 5A]
- GPIO: 3 Digital Input-Output TTL [3.3V]
- USB: USB CH340 + USB OTG
- UART: 3 RX/TX UART
- I2C: 2; I2C-1 Isolated input
- SPI: 2 SPI
- RS-232: UART1
- RS-485: UART2
- Board Indicator: Low power RGB LED PL9823-F5
- Control: ON/OFF button
- Reset: Outer Reset Pin
- Power: 5-24V 100 mA Power Pin / 5V 500mA USB

[x] OK - Open Collector

For more information see the MELA-board datasheet:
https://github.com/gmecc/mela/blob/main/images/board-env.jpg

MicroPython is implemented on top of the ESP-IDF, Espressif’s development framework for the ESP32.
This is a FreeRTOS based system. See the ESP-IDF Programming Guide for details.


.. csv-table:: GPIO
    :header: "Pin", "GPIO", "BOARD", "Type", "Function"
    :widths: 10, 15, 15, 10, 50

    "1", "GND"
    "2", "3V3"
    "3", "EN", "RESET", "I", "RESET"
    "4", "IO4", "MISO", "IsIO", "I2C"
    "5", "IO5", "MOSI", "IsIO", "I2C"
    "6", "IO6", "LED", "O", "LED RGB"
    "7", "IO7", "TX", "IsIO", "UART2 RS-485"
    "8", "IO15", "RX", "IsIO", "UART2 RS-485"
    "9", "IO16", "RTC", "IsIO", "UART2 RS-485"
    "10", "IO17", "TX", "IsIO", "UART1 RS-232"
    "11", "IO18", "RX", "IsIO", "UART1 RS-232"
    "12", "IO8", "?"
    "13", "IO19", , "IO", "USB Serial JTAG"
    "14", "IO20", , "IO", "USB Serial JTAG"
    "15", "IO3", "DI0", "IsI", "Didital Input 0-24V"
    "16", "IO46", "D1", "IsI", "Didital Input 0-24V"
    "17", "IO9", "D2", "IsI", "Didital Input 0-24V"
    "18", "IO10", "D3", "IsI", "Didital Input 0-24V"
    "19", "IO11", "D4", "IsI", "Didital Input 0-24V"
    "20", "IO12", "D5", "IsI", "Didital Input 0-24V"
    "21", "IO13", "D6", "IsI", "Didital Input 0-24V"
    "22", "IO14", "D7", "IsI", "Didital Input 0-24V"
    "23", "IO21", "D8", "IsI", "Didital Input 0-24V"
    "24", "IO47", "D9", "IsI", "Didital Input 0-24V"
    "25", "IO48", "PWM10", "OC", "PWM"
    "26", "IO48", "PWM10", "OC", "PWM"
    "27", "IO0", "BOOT", "T", "BOOT"
    "28", "IO35", "PWM12", "OC", "PWM"
    "29", "IO36", "PWM13", "OC", "PWM"
    "30", "IO37", "PWM14", "OC", "PWM"
    "31", "IO38", "PWM15", "OC", "PWM"
    "32", "IO39", "DI", "I", "Didital Input / JTAG"
    "33", "IO40", "DI", "I", "Didital Input / JTAG"
    "34", "IO41", "DI", "I", "Didital Input / JTAG"
    "35", "IO42", "DI", "I", "Didital Input / JTAG"
    "36", "RXD0", "RX0 ", "IsIO", "UART0"
    "37", "TXD0", "TX0", "IsIO", "UART0"
    "38", "IO2", "I2C", "IsIO", "I2C"
    "39", "IO1", "I2C", "IsIO", "I2C"
    "40", "GND", " ", " ", " "
    " ", " ", "VCC", "P", "VCC 24V 100mA "
    " ", " ", "GND", " ", "GND"


* *P*: Power supply;
* *I*: Input TTL;
* *I0*: Input/Output TTL;
* *IsI*: Isolated Input;
* *IsO*: Isolated Output;
* *IsIO*: Isolated Input/Output;
* *OC*: Open Collector Output;
* *T*: High Impedance Input (PULL APP);

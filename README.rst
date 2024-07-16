MELA
====

The `mela` module contains specific functions related to the hardware on a particular board.
To write portable code use functions and classes from the `mela` module.
To access platform-specific hardware use the appropriate library.


Classes
-------

* Pin
* PWM
* DAC
* ADC
* HMI
* I2C bus
* SPI bus
* RS-232 bus
* RS-485 bus
* RTC - часы реального времени
* Counter
   * счетчик импульсов
   * высокоскоростной счетчик импульсов
* Encoder - чтение данных с энкодера
* Timer
   * определение скорости
   * интервал времени
   * периодические процессы
* Impulse
   * выдача заданного чмсла импульсов
   * выдача определенного числа импульсов
* Speed - определение скорости
* Rotc - позиционирование

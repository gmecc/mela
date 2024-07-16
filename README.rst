MELA
====

The `mela` module contains specific functions related to the hardware on a particular board.
To write portable code use functions and classes from the `mela` module.
To access platform-specific hardware use the appropriate library.

Installation
------------

Install with mip
~~~~~~~~~~~~~~~~

.. code-block:: python

   import mip
   mip.install('github:gmecc/mela')


Install package without network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Установка прошивки с библиотекой mela
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Classes
-------

* ``Pin`` - управление входами и выходами
* ``Led`` - управление индикатором Led GRB
* ``HMI`` - подключение к HMI
* ``PWM``
   * генератор импульсов
   * генератор импульсов с заданной скважностью
* ``DAC`` - цифро-аналоговый преобразователь 12 бит
* ``ADC`` - аналого-цифровой преобразователь 16 бит
* ``RTC`` - часы реального времени
* ``Counter``
   * счетчик импульсов
   * высокоскоростной счетчик импульсов
* ``Encoder`` - чтение данных с энкодера
* ``Timer``
   * определение скорости
   * интервал времени
   * периодические процессы
   * выдачи импульсов заданной частоты
* ``Shedule`` - календарь
* ``Impulse``
   * выдача заданного числа импульсов
   * выдача определенного числа импульсов
* ``Speed`` - определение скорости
* ``Rotc`` - позиционирование
* ``Remote`` - выдача импульсов управляющих компанд
* ``I2C`` bus
* ``SPI`` bus
* ``RS-232`` bus
* ``RS-485`` bus
* ``Memory`` - информация о памяти
* ``Keyboard`` - десятичная клавиатура
* ``Indicator`` - 7-ми сегментный индикатор
* ``Pid`` - ПИД-регулятор
* ``Inv`` - обмен данными с преобразователями частоты
* ``Measure`` - обмен данными с датчиками по протоколу modbusRTU
* ``Pote`` - работа с внешним потенциометром
* ``Wake`` Работа с постоянным временем цикла

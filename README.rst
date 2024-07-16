MELA
====

The ``mela`` module contains specific functions related to the hardware on a particular board.
To write portable code use functions and classes from the ``mela`` module.
To access platform-specific hardware use the appropriate library.

Плата поставляется с установленной библиотекой ``mela``.


Installation
------------

Install with ``mip``
~~~~~~~~~~~~~~~~

.. code-block:: python

   import mip
   mip.install('github:gmecc/mela')


Установка из GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Скачайте библиотеку ``mela`` с репозитария
https://github.com/gmecc/mela/tree/main/firmware
и установите на плату.


Установка прошивки с библиотекой ``mela``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Скачайте и установите новую прошивку для платы:

https://github.com/gmecc/mela/blob/main/firmware/ESP32_GENERIC.bin


Classes
-------

* ``Pin`` - управление входами и выходами
* ``Button`` - устранение дребезга контактов
* ``Led`` - управление встроенным индикатором Led GRB
* ``HMI`` - подключение к HMI
* ``ADC`` - аналого-цифровой преобразователь 16 бит [0-10V; 0-20mA]
* ``DAC`` - цифро-аналоговый преобразователь 12 бит [0-10V]
* ``RTC`` - часы реального времени
* ``Shedule`` - календарь
* ``Timer`` - таймер
* ``PWM`` - генератор импульсов
* ``Counter`` - счетчик импульсов
* ``Encoder`` - чтение данных с энкодера
* ``Impulse`` - генератор пакетов импульсов
* ``Speed`` - определение скорости
* ``Remote`` - генератор импульсов управляющих команд
* ``Inv`` - обмен данными с преобразователями частоты
* ``Measure`` - обмен данными с датчиками по протоколу modbusRTU
* ``Pid`` - ПИД-регулятор
* ``Position`` - позиционирование
* ``Keyboard`` - десятичная клавиатура
* ``Indicator`` - 7-ми сегментный индикатор
* ``Potentiometer`` - работа с внешним потенциометром
* ``Memory`` - информация о памяти
* ``Wake`` - Работа с постоянным временем цикла
* ``I2C`` bus
* ``SPI`` bus
* ``RS-232`` bus
* ``RS-485`` bus

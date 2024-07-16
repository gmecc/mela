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


Install package without network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Скачайте и установите новую прошивку для платы:

https://github.com/gmecc/mela/blob/main/firmware/ESP32_GENERIC.bin


Установка прошивки с библиотекой ``mela``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Classes
-------

* ``Pin`` - управление входами и выходами
* ``Led`` - управление встроенным индикатором Led GRB
* ``HMI`` - подключение к HMI
* ``PWM`` - генератор импульсов
* ``DAC`` - цифро-аналоговый преобразователь 12 бит [0-10V]
* ``ADC`` - аналого-цифровой преобразователь 16 бит [0-10V]
* ``RTC`` - часы реального времени
* ``Counter`` - счетчик импульсов
* ``Encoder`` - чтение данных с энкодера
* ``Timer`` - таймер
* ``Shedule`` - календарь
* ``Impulse`` - генератор пакетов импульсов
* ``Speed`` - определение скорости
* ``Rotc`` - позиционирование
* ``Remote`` - генератор импульсов управляющих компанд
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
* ``Wake`` - Работа с постоянным временем цикла

MELA
====

The ``mela`` module contains specific functions related to the hardware on a particular board.
To write portable code use functions and classes from the ``mela`` module.
To access platform-specific hardware use the appropriate library.

The original ``MELA-board`` comes with the ``mela`` library installed.


Installation
------------

Install with ``mip``
~~~~~~~~~~~~~~~~
Install the ``mela`` library from the ``mip`` repository:

.. code-block:: python

   mip.install('github:gmecc/mela')



Installation from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download the ``mela`` library from the repository. Run this command to install

.. code-block:: python

   mpremote mip install github:Linnaar/mela_example


Installing firmware with the ``mela`` library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download new firmware for ``MELA-board``:

https://github.com/gmecc/mela/blob/main/firmware/ESP32_GENERIC.bin

Clear controller memory:

.. code-block:: python

   python -m esptool --chip esp32-s3 erase_flash

Install new firmware:

.. code-block:: python

   python -m esptool --chip esp32s3 -p <port> write_flash -z 0 <name_firmware>.bin


Classes
-------

* ``Pin`` - управление входами и выходами
* ``Button`` - устранение дребезга контактов
* ``Led`` - управление встроенным индикатором Led GRB
* ``HMI`` - подключение к HMI
* ``ADC`` - аналого-цифровой преобразователь
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
* ``I2C`` - обмен даммыми по протоколу I2C
* ``SPI`` - обмен даммыми по протоколу SPI
* ``RS-232`` - обмен даммыми через порт RS-232
* ``RS-485`` - обмен даммыми через порт RS-485
* ``Memory`` - информация о памяти
* ``Set`` - настройка параметров работы контроллера


Usage
-----

.. code-block:: python

   from mela import Mela
   plc=Mela()
   print(plc.info.free)


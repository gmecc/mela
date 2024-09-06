# ESP32-C3
# ****************************
# GPIO 0-1
# GPIO 3-7
# GPIO 10
# GPIO 18 - 21
# GPIO 0-8, 10, 11, 18, 19 - выводят уровень 1 при загрузке
# ****************************
# ADC1_CH0 - GPIO0
# ADC1_CH1 - GPIO1
# ADC1_CH2 - GPIO2
# ADC1_CH3 - GPIO3
# ADC1_CH4 - GPIO4
# ADC2_CH0 - GPIO5
# Timer 0-3
# LED - GPIO8
######################################################
'''
ДАТЧИК ДАВЛЕНИЯ И РАСХОДА ВОДЫ
modus RTU:
    - IREG #0 - давление [бар], период 1 мин
    - IREG #1 - расход [10л/мин], период 5 сек, выборка 10 измерений, период усреднения 1 мин
    - IREG #2 - объем [10л], период 1 час
    - IREG #3 - объем [10л], период 1 час / старшие разряды числа
Pin:
    GPIO0 - выход: led RGB
    GPIO1 - вход: датчик расхода воды (импульсный)
    GPIO2 - вход: датчик давления (аналоговый)
    GPIO3 - вход: датчик температуры DHT22
Счетчик достоверно считает импульсы до 500 Гц
Датчик расхода: 3960 импульсов на 10 литр
Датчик давления: 0,5-4,5В 5бар
'''
### IMPORT MODULES ###

import time, json, machine, dht, urandom, ntptime
from umodbus.tcp import ModbusTCP
import uasyncio as asyncio
from mypack import rgb, wifiConnect
from machine import Pin

wlan = wifiConnect('sensor-s3')
local_ip = wlan.wlan.ifconfig()[0]
ntptime.settime()

led = rgb.ledRGB(pin=48, pow=50)
led.blue()

# register_definitions
register_count = 10
holding = {'HREGS': {'HREG_NAME': {'register':0, 'len':register_count, 'val':[0 for i in range(register_count)]}}}
inputs = {'IREGS': {'IREGS_NAME': {'register':0, 'len':register_count, 'val':[0 for i in range(register_count)]}}}
coils = {'COILS': {'COILS_NAME': {'register':0, 'len':register_count, 'val':[0 for i in range(register_count)]}}}
discrete_input = {'ISTS': {'ISTS_NAME': {'register':0, 'len':register_count, 'val':[0 for i in range(register_count)]}}}

register_definitions = inputs | holding | coils | discrete_input
print('Register_definitions: OK')

slave = ModbusTCP()
slave.setup_registers(registers=register_definitions)
print('Register setup done')

# slave.set_ist(0, 0)   # discrete inputs #1x
# slave.set_ist(1, 0)   # discrete inputs #1x
# slave.set_coil(0, 0)  # coils #2x
# slave.set_coil(1, 0)  # coils #2x
slave.set_ireg(0, 0)  # inputs #3x
slave.set_ireg(1, 0)  # inputs #3x
# slave.set_ireg(2, 0)  # inputs #3x
# slave.set_ireg(3, 0)  # inputs #3x
# slave.set_ireg(4, 0)  # inputs #3x
slave.set_hreg(0, 0)  # holding #4x
slave.set_hreg(1, 0)  # holding #4x
# slave.set_hreg(2, 0)  # holding #4x
# slave.set_hreg(3, 0)  # holding #4x
volume = slave.get_ireg(3) # установка счетчика расхода воды
print('Setting initial values: OK')

# check whether client has been bound to an IP and a port
if not slave.get_bound_status():
    slave.bind(local_ip=local_ip, local_port=502)

def restart():
    print('Restart...')
    time.sleep(0.5)
    machine.reset()

# mode indicator
async def led_indicator(delay_ms):  
    while True:
        led.red()    
        await  asyncio.sleep_ms(int(delay_ms/15))
        led.green()
        await  asyncio.sleep_ms(int(delay_ms))

#####################################################

# чтение данных с датчиков
async def read_data(delay):
    while True:
        slave.set_ireg(0, urandom.randint(0, 100))
        slave.set_ireg(1, urandom.randint(100, 200))
        slave.set_hreg(0, urandom.randint(200, 300))
        slave.set_hreg(1, urandom.randint(300, 400))
        await  asyncio.sleep(delay)

# control devices
async def control_dev(duration):
    while True:
        # control dev 1
        if slave.get_coil(0) == 1:
            slave.set_coil(0, 0)
            
        # control dev 2
        if slave.get_coil(1) == 1:
            slave.set_coil(1, 0)
        
        # control dev 3
#         if slave.get_coil(2) == 1:
#             slave.set_coil(2, 0)

        await asyncio.sleep(duration)

# modbus_write 
async def modbus_write(delay):
    while  True:
        slave.process()
        print('\n') 
        print('================================')
        print(time.time())
#         print('coil #0: ',slave.get_coil(0))
#         print('coil #1: ',slave.get_coil(1))
#         print('coil #2: ',slave.get_coil(2))
        print('ireg #0: ',slave.get_ireg(0)) 
        print('ireg #1: ',slave.get_ireg(1))
        print('hreg #0: ',slave.get_hreg(0))
        print('hreg #1: ',slave.get_hreg(1)) 
#         print('ireg #2: ',slave.get_ireg(2)) 
#         print('ireg #3: ',slave.get_ireg(3)) 
#         print('ireg #4: ',slave.get_ireg(4)) 
        await  asyncio.sleep(delay) 

############################################################

while True:
    try:
        loop = asyncio.get_event_loop()
        
        loop.create_task(modbus_write(0.1))
        loop.create_task(read_data(1))
        loop.create_task(control_dev(1))
        loop.create_task(led_indicator(1000))
        
        loop.run_forever()
        
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP client...')
        led.blue()
        time.sleep(0.5)
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))
        led.red()
        time.sleep(0.5)
        restart()
        






 

  


   
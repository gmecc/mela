from bmp180 import BMP180
from machine import SoftI2C, Pin
import dht

class Mela:
  def __init__(self):
    self.environment=Environment()

class Environment:
  def __init__(self):
    i2c = SoftI2C(scl=Pin(18), sda=Pin(19), freq=100000)
    self.__bmp180 = BMP180(i2c)
    self._t_h = dht.DHT22(Pin(20))

  @property
  def temperature(self):
    return self.__bmp180.temperature

  @property
  def pressure(self):
    return self.__bmp180.pressure

  @property
  def altitude(self):
    return self.__bmp180.altitude

  @property
  def humidity(self):
    self._t_h.measure()
    return self._t_h.humidity()


plc = Mela()
plc.pressure()

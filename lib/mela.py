from bmp180 import BMP180
from machine import SoftI2C, Pin 
import dht 
import ds1302
import utime
import gc
import os
#======================================================================================================




#--------------------------------------------------------------------
#
#   Main class for our board
#
#--------------------------------------------------------------------
class Mela:
  def __init__(self):
    self.environment=Mela_environment()
    self.rtc=Mela_rtc()
    self.info=Mela_info()

#--------------------------------------------------------------------
#
#    Information class for our board
#
#--------------------------------------------------------------------
class Mela_info:
  def __init__(self):
    if not gc.isenabled(): gc.enable()
    gc.collect()

  @property
  def df(self):
    s = os.statvfs('//')
    T=(s[1]*s[2])/1048576
    F=(s[0]*s[3])/1048576
    P = '{0:.2f}%'.format(F/T*100)
    return ('VFS: Total:{0} Mb Free:{1} Mb ({2})'.format(T,F,P))

  @property
  def free(self):
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(F/T*100)
    return ('RAM: Total:{0} bytes Free:{1} bytes ({2})'.format(T,F,P))


#--------------------------------------------------------------------
#
#    RTC class for DS1302
#
#--------------------------------------------------------------------
class Mela_rtc:
  def __init__(self):
    self.__ds1302_rtc = ds1302.DS1302(Pin(21), Pin(22), Pin(23))  # (clk, dio, cs)

# convert library output to human readable form
  @property
  def now(self):
    return str(self.__ds1302_rtc.year())+"-"+str('%0*d' % (2, self.__ds1302_rtc.month()))+"-"+str('%0*d' % (2, self.__ds1302_rtc.day()))+" "+str('%0*d' % (2, self.__ds1302_rtc.hour()))+":"+str('%0*d' % (2, self.__ds1302_rtc.minute()))+":"+str('%0*d' % (2, self.__ds1302_rtc.second())) 

# convert library output to standart micropython tuple (year, month, mday, hour, minute, second, weekday, yearday)
  @property
  def now_raw(self):
    return [self.__ds1302_rtc.year(),self.__ds1302_rtc.month(),self.__ds1302_rtc.day(),self.__ds1302_rtc.hour(),self.__ds1302_rtc.minute(),self.__ds1302_rtc.second(),self.__ds1302_rtc.weekday(),0] 

# convert library output to standart unix unixtime
  @property
  def now_unixtime(self):
    return utime.mktime(self.now_raw)+946684800

# convert library output to unixtime for Embeded boards (since 2000-01-01)
  @property
  def now_em_unixtime(self):
    return utime.mktime(self.now_raw)

#--------------------------------------------------------------------
#
#    Environment class for MBM180
#
#--------------------------------------------------------------------
class Mela_environment:
  def __init__(self):
    i2c = SoftI2C(scl=Pin(18), sda=Pin(19), freq=100000)
    self.__bmp180 = BMP180(i2c)
    self.__dht = dht.DHT11(Pin(14))

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
    self.__dht.measure()
    return self.__dht.humidity()

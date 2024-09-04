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
    self.info=Mela_info()
    self.config=Mela_config()
    self.rtc=Mela_rtc()
    
    
    self.modbus_slave485=False
    self.modbus_master485=False
    if self.config.modbus['connect_type']=='slave485':              
      self.modbus_slave485=Mela_modbus_slave485(config=self.config.modbus_slave485)
    elif self.config.modbus['connect_type']=='master485':
      self.modbus_master485=Mela_modbus_master485(config=self.config.modbus_master485)
    
    self.wifi=False 
    if self.config.wifi['connect_on_boot']:
      self.wlan_connect()
      
#********************************************************************      
  def wlan_disconnect(self):
    import network
    
    sta_if=network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.disconnect()
    sta_if.active(False)

#********************************************************************      
  def wlan_connect(self):
    import network
    import utime as time
    
    sta_if=network.WLAN(network.STA_IF)
    sta_if.active(True)
    if sta_if.isconnected():
      print('WLAN already connected. Board IP: %s' % sta_if.ifconfig()[0])
      return True  
    try:
      wlan_found=False
      print("Scanning WLANs")
      wlans=self.info.wlan_scan(False)
      for ssid, bssid, channel, rssi, authmode, hidden in sorted(wlans, key=lambda x: x[3], reverse=True):        
        ssid = ssid.decode('utf-8')
        if ssid==self.config.wifi['networks'][0]['ssid']:
          print("WLAN ssid: %s found at chan: %d rssi: %d bssid: %s" % (ssid, channel, rssi, bssid.hex('-')))
          wlan_found=True
      if not wlan_found:
        print("WLAN %s not found!" % self.config.wifi['networks'][0]['ssid'])
        return False
      print('Trying to connect...')
      start = time.ticks_ms()
      sta_if.connect(self.config.wifi['networks'][0]['ssid'],self.config.wifi['networks'][0]['key'])
      for _ in range(10000):
        if sta_if.isconnected():
          print('\nConnected! Time: %d ms. Board IP: %s' % (time.ticks_diff(time.ticks_ms(), start), sta_if.ifconfig()[0]))
          self.wifi=sta_if
          return True
        else:
          print('.', end='')
          time.sleep_ms(100)
      print('\nConnection timeout!')
      sta_if.disconnect()
      sta_if.active(False)
      return False
    except OSError as e:
      print("\nWLAN connection problem. ", str(e)) 
      return False 
    

#--------------------------------------------------------------------
#
#    Configuration save/load class for our board
#
#--------------------------------------------------------------------
class Mela_config:
  def __init__(self):
    self.data=self.load_config()
    
#********************************************************************
  @property
  def wifi(self):
    return self.data['config']['wifi']

#********************************************************************
  @property
  def modbus(self):
    return self.data['config']['modbus']

#********************************************************************
  @property
  def modbus_slave485(self):
    return self.data['config']['modbus']['slave485']

#********************************************************************
  @property
  def modbus_master485(self):
    return self.data['config']['modbus']['master485']

#********************************************************************
  def load_config(self):
    import ujson as json
    
    try:
      with open('config.json','r') as settings_file:
        return json.load(settings_file)
    except:
      print("Failed reading configuration file. Returning default configuration.")
      return {'config': {
          'wifi': {'connect_on_boot': False, 'networks': [{'ssid': 'LAN', 'key': '12345'}]},
          'modbus': {'connect_type':False, 'slave485':{'load_definitions_from_config':True, 'address': 10, 'baudrate': 9600, 'data_bits': 8, 'stop_bits': 1, 'parity': None, 'register_definitions':{ "IREGS": {"TIMESTAMP": {"register": 1,"len": 2,"val": 0}, "FREE_RAM": {"register": 3,"len": 1,"val": 0},"FREE_VFS": {"register": 4,"len": 1,"val": 0} } }}, 'master485':{'baudrate': 9600, 'data_bits': 8, 'stop_bits': 1, 'parity': None } }
          }
      } 

#********************************************************************
  def save_config(self):
    import ujson as json
    
    try:
      with open('config.json','w') as settings_file:
        return json.dump(self.data,settings_file)
    except:
      print("Failed writing configuration file.")
      return False

#--------------------------------------------------------------------
#
#    Information class for our board
#
#--------------------------------------------------------------------
class Mela_info:
  def __init__(self):
    if not gc.isenabled(): gc.enable()
    gc.collect()
    
#********************************************************************
  def df(self, prn=True):
    s = os.statvfs('//')
    T=(s[1]*s[2])/1048576
    F=(s[0]*s[3])/1048576
    P = '{0:.2f}'.format(F/T*100)
    if prn:
      return ('VFS: Total:{0} Mb Free:{1} Mb ({2}%)'.format(T,F,P))
    else:
      return P

#********************************************************************
  def free(self, prn=True):
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}'.format(F/T*100)
    if prn:
      return ('RAM: Total:{0} bytes Free:{1} bytes ({2}%)'.format(T,F,P))
    else:
      return P

#********************************************************************
  def wlan_scan(self, prn=True):
    import network
    try:
      sta_if=network.WLAN(network.STA_IF)
      sta_if.active(True)
      print("WLAN interface activated. Starting scan...")      
      wlans=sta_if.scan()
      if prn:
        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        count=0
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(wlans, key=lambda x: x[3], reverse=True):
          count=count+1
          ssid = ssid.decode('utf-8')      
          print("%d ssid: %s chan: %d rssi: %d authmode: %s bssid: %s" % (count, ssid, channel, rssi, AUTHMODE.get(authmode, '?'), bssid.hex('-')))
      else:
        return wlans
    except OSError as e:
      print("WLAN connection problem. ", str(e))

#********************************************************************        
  def wlan_status(self):
      import network
      try:
        sta_if=network.WLAN(network.STA_IF)
        sta_if.active(True)
        STATUS={1000: "STAT_IDLE", 1001: " STAT_CONNECTING", 202: "STAT_WRONG_PASSWORD", 201: "STAT_NO_AP_FOUND", 1010: "STAT_GOT_IP", 203: "STAT_ASSOC_FAIL", 200: "STAT_BEACON_TIMEOUT", 204: "STAT_HANDSHAKE_TIMEOUT"}
        PM_MODES={0: 'PM_NONE', 1: 'PM_PERFORMANCE', 2: 'PM_POWERSAVE'}
        print("Current WLAN status: %s, power mode: %s, TX power: %s, MAC %s, ssid: %s, ch: %s" % (STATUS.get(sta_if.status(), '?'), PM_MODES.get(sta_if.config('pm'), '?'),sta_if.config('txpower'),sta_if.config('mac').hex('-'),sta_if.config('ssid'),sta_if.config('channel')))
      except OSError as e:
        print("WLAN connection problem. ", str(e))
    
    
#--------------------------------------------------------------------
#
#    RTC class for DS1307
#
#--------------------------------------------------------------------
class Mela_rtc:
  def __init__(self):
    from ds1307 import DS1307
    from machine import SoftI2C, Pin
    i2c = SoftI2C(scl=Pin(4), sda=Pin(5), freq=800000)
    self.__ds1307_rtc = DS1307(addr=0x68, i2c=i2c)

# convert library output to human readable form
  @property
  def now(self):
    return str(self.__ds1307_rtc.year)+"-"+str('%0*d' % (2, self.__ds1307_rtc.month))+"-"+str('%0*d' % (2, self.__ds1307_rtc.day))+" "+str('%0*d' % (2, self.__ds1307_rtc.hour))+":"+str('%0*d' % (2, self.__ds1307_rtc.minute))+":"+str('%0*d' % (2, self.__ds1307_rtc.second))

# convert library output to standart micropython tuple (year, month, mday, hour, minute, second, weekday, yearday)
  @property
  def now_raw(self):
    return self.__ds1307_rtc.datetime

# convert library output to standart unix unixtime
  @property
  def now_unixtime(self):
    import utime
    return utime.mktime(self.now_raw)+946684800

# convert library output to unixtime for Embeded boards (since 2000-01-01)
  @property
  def now_em_unixtime(self):
    import utime
    return utime.mktime(self.now_raw)


#--------------------------------------------------------------------
#
#    Modbus Slave485 class 
#
#--------------------------------------------------------------------
class Mela_modbus_slave485:
  def __init__(self,config=False):
    from umodbus.serial import ModbusRTU   
     
    self.connection = ModbusRTU(
          addr=config['address'],        # address on bus
          pins=(16,15),          # given as tuple (TX-DI, RX-RO)
          baudrate=config['baudrate'],        # optional, default 9600
          data_bits=config['data_bits'],          # optional, default 8
          stop_bits=config['stop_bits'],          # optional, default 1
          parity=config['parity'],          # optional, default None
          ctrl_pin=7,          # optional, control DE/RE
          uart_id=1         # optional, default 1, see port specific documentation
    )
    
    if config['load_definitions_from_config']:
      self.connection.setup_registers(registers=config['register_definitions'])
      


#--------------------------------------------------------------------
#
#    Modbus Master485 class 
#
#--------------------------------------------------------------------
class Mela_modbus_master485:
  def __init__(self,config=False):
    from umodbus.serial import Serial as ModbusRTUMaster   
     
    self.connection = ModbusRTUMaster(          
          pins=(16,15),          # given as tuple (TX-DI, RX-RO)
          baudrate=config['baudrate'],        # optional, default 9600
          data_bits=config['data_bits'],          # optional, default 8
          stop_bits=config['stop_bits'],          # optional, default 1
          parity=config['parity'],          # optional, default None
          ctrl_pin=7,          # optional, control DE/RE
          uart_id=1         # optional, default 1, see port specific documentation
    )
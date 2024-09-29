import gc
import os
#======================================================================================================

#--------------------------------------------------------------------
#
#   Main class for Mela board
#
#--------------------------------------------------------------------
class Mela:
    """
    Main class for Mela board.
    """

    def __init__(self):
        """
        Initialize the Mela board with its components and configurations.
        """
        self.info = MelaInfo()
        self.config = MelaConfig()
        self.rtc = MelaRTC()

        self.wifi = False
        if self.config.wifi['connect_on_boot']:
            self.wlan_connect()

        self.modbus_slave485 = None
        self.modbus_master485 = None
        self.modbus_slaveTCP = None
        self.modbus_masterTCP = None

        connect_type = self.config.modbus['connect_type']
        if connect_type == 'slave485':
            self.modbus_slave485 = MelaModbusSlave485(config=self.config.modbus_slave485)
        elif connect_type == 'master485':
            self.modbus_master485 = MelaModbusMaster485(config=self.config.modbus_master485)
        elif connect_type == 'slaveTCP':
            self.modbus_slaveTCP = MelaModbusSlaveTCP(config=self.config.modbus_slaveTCP, wifi=self.wifi)
        elif connect_type == 'masterTCP':
            self.modbus_masterTCP = MelaModbusMasterTCP(config=self.config.modbus_masterTCP, wifi=self.wifi)

#********************************************************************
    def wlan_disconnect(self) -> None:
        """
        Disconnect from the WLAN and deactivate the interface.
        """
        import network

        try:
            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            sta_if.disconnect()
            sta_if.active(False)
        except Exception as e:
            raise ConnectionError('Failed to disconnect from WLAN: {}'.format(str(e)))

#********************************************************************
    def wlan_connect(self) -> bool:
        """
        Connect to the WLAN using the configuration provided.

        :return: True if connected successfully, False otherwise.
        """
        import network
        import utime as time

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        
        if sta_if.isconnected():
            print('WLAN already connected. Board IP: {}'.format(sta_if.ifconfig()[0]))
            self.wifi = sta_if
            return True
        
        try:
            wlan_found = False
            print('Scanning WLANs')
            wlans = self.info.wlan_scan(False)
            
            for ssid, bssid, channel, rssi, authmode, hidden in sorted(wlans, key=lambda x: x[3], reverse=True):
                ssid = ssid.decode('utf-8')
                ssid_cf = [wlan for wlan in self.config.wifi['networks'] if wlan['ssid'] == ssid]
                
                if ssid_cf:
                    print("WLAN ssid: %s found at chan: %d rssi: %d bssid: %s" % (ssid, channel, rssi, bssid.hex('-')))
                    wlan_found = True
                    break
            
            if not wlan_found:
                print('WLAN not found!')
                return False
            
            print('Trying to connect...')
            start = time.ticks_ms()
            sta_if.connect(ssid_cf[0]['ssid'], ssid_cf[0]['key'])
            
            for _ in range(100):
                if sta_if.isconnected():
                    print('\nConnected! Time: %d ms. Board IP: %s' % (time.ticks_diff(time.ticks_ms(), start), sta_if.ifconfig()[0]))
                    self.wifi = sta_if
                    return True
                else:
                    print('.', end='')
                    time.sleep_ms(100)
            
            print('\nConnection timeout!')
            sta_if.disconnect()
            sta_if.active(False)
            return False
        
        except OSError as e:
            raise ConnectionError('\nWLAN connection problem: {}'.format(str(e)))


#--------------------------------------------------------------------
#
#    Configuration save/load class for Mela board
#
#--------------------------------------------------------------------
class MelaConfig:
    """
    A class to manage saving and loading configuration for the Mela board.
    """

    def __init__(self):
        """
        Initialize the MelaConfig class and load the configuration.
        """
        self.data = self.load_config()

    @property
    def wifi(self) -> Dict[str, Any]:
        """
        Get the WiFi configuration.

        :return: WiFi configuration dictionary.
        """
        return self.data['config']['wifi']

    @property
    def modbus(self) -> Dict[str, Any]:
        """
        Get the Modbus configuration.

        :return: Modbus configuration dictionary.
        """
        return self.data['config']['modbus']

    @property
    def modbus_slave485(self) -> Dict[str, Any]:
        """
        Get the Modbus Slave 485 configuration.

        :return: Modbus Slave 485 configuration dictionary.
        """
        return self.data['config']['modbus']['slave485']

    @property
    def modbus_master485(self) -> Dict[str, Any]:
        """
        Get the Modbus Master 485 configuration.

        :return: Modbus Master 485 configuration dictionary.
        """
        return self.data['config']['modbus']['master485']

    @property
    def modbus_slaveTCP(self) -> Dict[str, Any]:
        """
        Get the Modbus Slave TCP configuration.

        :return: Modbus Slave TCP configuration dictionary.
        """
        return self.data['config']['modbus']['slaveTCP']

    @property
    def modbus_masterTCP(self) -> Dict[str, Any]:
        """
        Get the Modbus Master TCP configuration.

        :return: Modbus Master TCP configuration dictionary.
        """
        return self.data['config']['modbus']['masterTCP']

    def load_config(self) -> Dict[str, Any]:
        """
        Load the configuration from the 'config.json' file.

        :return: Configuration dictionary.
        """
        import ujson as json

        try:
            with open('config.json', 'r') as settings_file:
                return json.load(settings_file)
        except (OSError, json.JSONDecodeError) as e:
            print('Failed reading configuration file: {}. Returning default configuration.'.format(e))
            return {
                'config': {
                    'wifi': {'connect_on_boot': False, 'networks': [{'ssid': 'LAN', 'key': '12345'}]},
                    'modbus': {
                        'connect_type': False,
                        'slave485': {
                            'load_definitions_from_config': True,
                            'address': 10,
                            'baudrate': 9600,
                            'data_bits': 8,
                            'stop_bits': 1,
                            'parity': None,
                            'register_definitions': {
                                'IREGS': {
                                    'TIMESTAMP': {'register': 1, 'len': 2, 'val': 0},
                                    'FREE_RAM': {'register': 3, 'len': 1, 'val': 0},
                                    'FREE_VFS': {'register': 4, 'len': 1, 'val': 0}
                                }
                            }
                        },
                        'master485': {'baudrate': 9600, 'data_bits': 8, 'stop_bits': 1, 'parity': None},
                        'slaveTCP': {
                            'load_definitions_from_config': True,
                            'port': 502,
                            'register_definitions': {
                                'IREGS': {
                                    'TIMESTAMP': {'register': 1, 'len': 2, 'val': 0},
                                    'FREE_RAM': {'register': 3, 'len': 1, 'val': 0},
                                    'FREE_VFS': {'register': 4, 'len': 1, 'val': 0}
                                }
                            }
                        },
                        'masterTCP': {'port': 502, 'slave_ip': False, 'timeout': 5, 'always_reconnect': False}
                    }
                }
            }

    def save_config(self) -> bool:
        """
        Save the current configuration to the 'config.json' file.

        :return: True if the configuration was saved successfully, False otherwise.
        """
        import ujson as json

        try:
            with open('config.json', 'w') as settings_file:
                json.dump(self.data, settings_file)
            return True
        except OSError as e:
            print('Failed writing configuration file: {}'.format(e))
            return False

#--------------------------------------------------------------------
#
#    Information class for Mela board
#
#--------------------------------------------------------------------
class MelaInfo:
    """
    A class to provide information about the Mela board.
    """

    def __init__(self):
        """
        Initialize the MelaInfo class and enable garbage collection if not already enabled.
        """
        if not gc.isenabled():
            gc.enable()
        gc.collect()

    #********************************************************************
    def df(self, prn: bool = True) -> Union[str, float]:
        """
        Get the filesystem usage information.

        :param prn: Boolean indicating whether to print the information.
        :return: Filesystem usage information as a string or percentage free space as a float.
        """
        s = os.statvfs('//')
        total = (s[1] * s[2]) / 1048576
        free = (s[0] * s[3]) / 1048576
        percent_free = (free / total) * 100
        if prn:
            return f'VFS: Total: {total:.2f} Mb Free: {free:.2f} Mb ({percent_free:.2f}%)'
        else:
            return f'{percent_free:.2f}'

    #********************************************************************
    def free(self, prn: bool = True) -> Union[str, float]:
        """
        Get the RAM usage information.

        :param prn: Boolean indicating whether to print the information.
        :return: RAM usage information as a string or percentage free space as a float.
        """
        gc.collect()
        free = gc.mem_free()
        allocated = gc.mem_alloc()
        total = free + allocated
        percent_free = (free / total) * 100
        if prn:
            return f'RAM: Total: {total} bytes Free: {free} bytes ({percent_free:.2f}%)'
        else:
            return f'{percent_free:.2f}'

    #********************************************************************
    def wlan_scan(self, prn: bool = True) -> Union[None, list]:
        """
        Scan for available WLAN networks.

        :param prn: Boolean indicating whether to print the scan results.
        :return: List of WLAN networks if prn is False, otherwise None.
        """
        import network
        try:
            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            print('WLAN interface activated. Starting scan...')
            wlans = sta_if.scan()
            if prn:
                AUTHMODE = {0: 'open', 1: 'WEP', 2: 'WPA-PSK', 3: 'WPA2-PSK', 4: 'WPA/WPA2-PSK'}
                for count, (ssid, bssid, channel, rssi, authmode, hidden) in enumerate(sorted(wlans, key=lambda x: x[3], reverse=True), start=1):
                    ssid = ssid.decode('utf-8')
                    print(f'{count} ssid: {ssid} chan: {channel} rssi: {rssi} authmode: {AUTHMODE.get(authmode, "?")} bssid: {bssid.hex("-")}')
            else:
                return wlans
        except OSError as e:
            raise ConnectionError(f'WLAN connection problem: {str(e)}')
    #********************************************************************
    def wlan_status(self) -> None:
        """
        Print the current WLAN status.
        """
        import network
        try:
            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            STATUS = {
                1000: 'STAT_IDLE', 1001: 'STAT_CONNECTING', 202: 'STAT_WRONG_PASSWORD',
                201: 'STAT_NO_AP_FOUND', 1010: 'STAT_GOT_IP', 203: 'STAT_ASSOC_FAIL',
                200: 'STAT_BEACON_TIMEOUT', 204: 'STAT_HANDSHAKE_TIMEOUT'
            }
            PM_MODES = {0: 'PM_NONE', 1: 'PM_PERFORMANCE', 2: 'PM_POWERSAVE'}
            print("Current WLAN status: %s, power mode: %s, TX power: %s, MAC %s, ssid: %s, ch: %s" % (STATUS.get(sta_if.status(), '?'), PM_MODES.get(sta_if.config('pm'), '?'),sta_if.config('txpower'),sta_if.config('mac').hex('-'),sta_if.config('ssid'),sta_if.config('channel')))

        except OSError as e:
            raise ConnectionError(f'WLAN connection problem: {str(e)}')


#--------------------------------------------------------------------
#
#    RTC class for DS1307
#
#--------------------------------------------------------------------
class MelaRTC:
    """
    A class to manage the DS1307 RTC module.
    """

    def __init__(self):
        """
        Initialize the DS1307 RTC module.
        """
        from ds1307 import DS1307
        from machine import SoftI2C, Pin
        import utime as time

        i2c = SoftI2C(scl=Pin(4), sda=Pin(5), freq=800000)
        self.__ds1307_rtc = DS1307(addr=0x68, i2c=i2c)

    @property
    def now(self) -> str:
        """
        Get the current date and time in human-readable form.

        :return: Current date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'.
        """
        return str(self.__ds1307_rtc.year)+"-"+str('%0*d' % (2, self.__ds1307_rtc.month))+"-"+str('%0*d' % (2, self.__ds1307_rtc.day))+" "+str('%0*d' % (2, self.__ds1307_rtc.hour))+":"+str('%0*d' % (2, self.__ds1307_rtc.minute))+":"+str('%0*d' % (2, self.__ds1307_rtc.second))

    @property
    def now_raw(self) -> Tuple[int, int, int, int, int, int, int, int]:
        """
        Get the current date and time as a tuple.

        :return: Current date and time as a tuple (year, month, mday, hour, minute, second, weekday, yearday).
        """
        return self.__ds1307_rtc.datetime

    @property
    def now_unixtime(self) -> int:
        """
        Get the current Unix time.

        :return: Current Unix time.
        """
        import utime as time

        return time.mktime(self.now_raw) + 946684800

    @property
    def now_em_unixtime(self) -> int:
        """
        Get the current Unix time for embedded boards (since 2000-01-01).

        :return: Current Unix time for embedded boards.
        """
        import utime as time

        return time.mktime(self.now_raw)

#--------------------------------------------------------------------
#
#    Modbus Slave485 class
#
#--------------------------------------------------------------------
class MelaModbusSlave485:
    """
    A class to manage Modbus RTU slave connections over RS485.
    """

    def __init__(self, config: dict = None):
        """
        Initialize the Modbus RTU slave with the given configuration.

        :param config: Configuration dictionary containing 'address', 'baudrate', 'data_bits', 'stop_bits', 'parity', 'load_definitions_from_config', and 'register_definitions'.
        """
        from umodbus.serial import ModbusRTU

        if not config:
            raise ValueError('Error. Configuration is required.')

        self.connection = ModbusRTU(
            addr=config['address'],  # address on bus
            pins=(16, 15),  # given as tuple (TX-DI, RX-RO)
            baudrate=config.get('baudrate', 9600),  # optional, default 9600
            data_bits=config.get('data_bits', 8),  # optional, default 8
            stop_bits=config.get('stop_bits', 1),  # optional, default 1
            parity=config.get('parity', None),  # optional, default None
            ctrl_pin=7,  # optional, control DE/RE
            uart_id=1  # optional, default 1, see port specific documentation
        )

        if config['load_definitions_from_config']:
            self.connection.setup_registers(registers=config['register_definitions'])



#--------------------------------------------------------------------
#
#    Modbus Master485 class
#
#--------------------------------------------------------------------
class MelaModbusMaster485:
    """
    A class to manage Modbus RTU master connections over RS485.
    """

    def __init__(self, config: dict = None):
        """
        Initialize the Modbus RTU master with the given configuration.

        :param config: Configuration dictionary containing 'baudrate', 'data_bits', 'stop_bits', and 'parity'.
        """
        from umodbus.serial import Serial as ModbusRTUMaster

        if not config:
            raise ValueError('Error. Configuration is required.')

        self.connection = ModbusRTUMaster(
            pins=(16, 15),  # given as tuple (TX-DI, RX-RO)
            baudrate=config.get('baudrate', 9600),  # optional, default 9600
            data_bits=config.get('data_bits', 8),  # optional, default 8
            stop_bits=config.get('stop_bits', 1),  # optional, default 1
            parity=config.get('parity', None),  # optional, default None
            ctrl_pin=7,  # optional, control DE/RE
            uart_id=1  # optional, default 1, see port specific documentation
        )


#--------------------------------------------------------------------
#
#    Modbus SlaveTCP class
#
#--------------------------------------------------------------------
class MelaModbusSlaveTCP:
    """
    A class to manage Modbus TCP slave connections.
    """

    def __init__(self, config: dict = None, wifi: bool = False):
        """
        Initialize the Modbus TCP slave with the given configuration and wifi status.

        :param config: Configuration dictionary containing 'port', 'load_definitions_from_config', and 'register_definitions'.
        :param wifi: Wifi connection object.
        """
        from umodbus.tcp import ModbusTCP

        if not wifi:
            raise ConnectionError('Error. Wifi not connected.')

        if not config:
            raise ValueError('Error. Configuration is required.')

        self.connection = ModbusTCP()
        if not self.connection.get_bound_status():
            self.connection.bind(local_ip=wifi.ifconfig()[0], local_port=config['port'])

        if config.get('load_definitions_from_config'):
            self.connection.setup_registers(registers=config['register_definitions'])


#--------------------------------------------------------------------
#
#    Modbus MasterTCP class
#
#--------------------------------------------------------------------
class MelaModbusMasterTCP:
    """
    A class to manage Modbus TCP connections.
    """

    def __init__(self, config: dict = None, wifi: bool = False):
        """
        Initialize the Modbus TCP master with the given configuration and wifi status.

        :param config: Configuration dictionary containing 'slave_ip', 'port', 'timeout', and 'always_reconnect'.
        :param wifi: Boolean indicating if wifi is connected.
        """
        if config is None:
            raise ValueError('Error. Configuration is required.')
        
        self.connection = self.reconnect(config, wifi)


    def reconnect(self, config: dict = None, wifi: bool = False) -> bool:
        """
        Reconnect to the Modbus TCP slave.

        :param config: Configuration dictionary containing 'slave_ip', 'port', and 'timeout', and 'always_reconnect'.
        :param wifi: Boolean indicating if wifi is connected.
        :return: Connection status.
        """
        from umodbus.tcp import TCP as ModbusTCPMaster
        import utime as time

        if not wifi:
            raise ConnectionError('Error. Wifi not connected.')

        if config is None:
            raise ValueError('Error. Configuration is required.')
        
        while True:
          try:
            connection = ModbusTCPMaster(
                slave_ip=config['slave_ip'],
                slave_port=config['port'],
                timeout=config.get('timeout', 5.0)  # optional, timeout in seconds, default 5.0
            )
            return connection
          except Exception as e:
            print('Error reconnecting to slave. {}'.format(e))
            if not config.get('always_reconnect', False):
              raise
            print('Retrying in 5 seconds...')
            time.sleep(5)  # Optional: wait before retrying

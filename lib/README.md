# Mela 
Library for the Mela board, providing initialization and configuration management for various components such as Modbus and WLAN.

# Install

Run this command to install `mpremote mip install github:Linnaar/mela_example`

# Usage

Example of usage:

```
from mela import Mela
plc=Mela()
print(plc.info.free())
```

## Classes

### `Mela`

The main class for the Mela board.

#### Methods

- `__init__()`: Initializes the Mela board with its components and configurations. 
- `wlan_disconnect()`: Disconnects from the WLAN and deactivates the interface.
- `wlan_connect()`: Connects to the WLAN using the configuration provided.

### `MelaConfig`

A class to manage saving and loading configuration for the Mela board.

#### Methods

- `__init__()`: Initializes the MelaConfig class and loads the configuration.
- `load_config()`: Loads configuration from `config.json` file, or fall back to a default configuration if there are issues with reading or decoding the configuration file.
- `save_config()`: Saves the current configuration to the `config.json` file.

#### Properties

- `wifi`: Returns the WiFi configuration.
- `modbus`: Returns the Modbus configuration (485 and TCP).
- `modbus_slave485`: Returns the Modbus Slave 485 configuration.
- `modbus_master485`: Returns the Modbus Master 485 configuration.
- `modbus_slaveTCP`: Returns the Modbus Slave TCP configuration.
- `modbus_masterTCP`: Returns the Modbus Master TCP configuration.

### `MelaInfo`

A class to provide information about the Mela board.

#### Methods

- `__init__()`: Initializes the MelaInfo class and enables garbage collection if not already enabled.
- `df(prn: bool = True)`: Gets the filesystem usage information.
- `free(prn: bool = True)`: Gets the RAM usage information.
- `wlan_scan(prn: bool = True)`: Scans for available WLAN networks.
- `wlan_status()`: Prints the current WLAN status.

### `MelaRTC`

A class to manage the DS1307 RTC module on the Mela board.

#### Methods

- `__init__()`: Initialize the DS1307 RTC module

#### Properties

- `now`: Get the current date and time in human-readable form.
- `now_raw`: Get the current date and time as a tuple.
- `now_unixtime`: Get the current Unix time.
- `now_em_unixtime`: Get the current Unix time for embedded boards (since 2000-01-01).

### `MelaModbusSlave485`

A class to manage Modbus RTU slave connections over RS485.

#### Methods
- `__init__(config: Dict[str, Any])`: Initializes the Modbus Slave 485 with the provided configuration.

### `MelaModbusMaster485`

A class to manage Modbus RTU master connections over RS485.

#### Methods
- `__init__(config: Dict[str, Any])`: Initializes the Modbus Master 485 with the provided configuration.

### `MelaModbusSlaveTCP`

A class to manage Modbus TCP slave connections.

#### Methods
- `__init__(config: Dict[str, Any], wifi: bool)`: Initializes the Modbus Slave TCP with the provided configuration and WiFi status.


### `MelaModbusMasterTCP`

A class to manage Modbus TCP master connections.

#### Methods
- `__init__(config: Dict[str, Any], wifi: bool)`: Initializes the Modbus Master TCP with the provided configuration and WiFi status.
- `reconnect(self, config: dict = None, wifi: bool = False) -> bool`: Reconnect to the Modbus TCP slave.

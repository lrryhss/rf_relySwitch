# Radar Switch Control System

This project provides a Python library and Arduino firmware for controlling radar switch relays.

## Installation

### Python Package
```bash
pip install radarswitch
```

### Arduino Firmware (PlatformIO)
1. Install [PlatformIO IDE](https://platformio.org/install)
2. Clone this repository
3. Open the project in PlatformIO
4. Configure platformio.ini for Arduino Nano:
```ini
[env:nanoatmega328]
platform = atmelavr
board = nanoatmega328
framework = arduino
monitor_speed = 9600
lib_deps = 
    bblanchon/ArduinoJson@^6.21.3
```
5. Build and upload the firmware

## Hardware Configuration
- Relay 1: Pin 2
- Relay 2: Pin 3
- Relay 3: Pin 4
- Relay 4: Pin 5

## Communication Protocol

### Setting Relay States
Send JSON command to set relay states:
```json
{
  "relays": {
    "relay1": 1,  // 1 = ON, 0 = OFF
    "relay2": 0,
    "relay3": 1,
    "relay4": 0
  }
}
```

### Reading Relay Status
Send JSON command to get relay status:
```json
{
  "command": "status"
}
```

Response format:
```json
{
  "status": {
    "relay1": 1,  // 1 = ON, 0 = OFF
    "relay2": 0,
    "relay3": 1,
    "relay4": 0
  }
}
```

## Required Libraries
- ArduinoJson (v6.21.3) - For JSON parsing and serialization

## Python Library Usage

```python
from radarswitch import RadarSwitch

# Create connection
with RadarSwitch('COM25') as rs:
    # Get and print status
    status = rs.get_status()
    rs.print_status(status)
    
    # Control relays
    rs.set_relay(1, True)  # Turn on relay 1
    rs.set_relay(2, False) # Turn off relay 2
    
    # Get specific relay state
    if rs.get_relay(1):
        print("Relay 1 is ON")
```

## API Reference

### RadarSwitch Class

#### `__init__(port: str, baudrate: int = 9600, timeout: float = 1.0)`
Initialize the radar switch controller.

- `port`: Serial port name (e.g. 'COM25')
- `baudrate`: Baud rate for serial communication (default: 9600)
- `timeout`: Serial timeout in seconds (default: 1.0)

#### Methods

- `connect()`: Establish serial connection
- `close()`: Close serial connection
- `set_relay(relay_num: int, state: bool)`: Set relay state
- `get_relay(relay_num: int) -> bool`: Get state of specific relay
- `get_status() -> Dict[str, int]`: Get current relay status
- `print_status(status: Optional[Dict[str, int]] = None)`: Print formatted relay status

## Example

See [examples/basic_usage.py](examples/basic_usage.py) for a complete usage example.

## License
MIT License - See LICENSE file for details

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
# Radar Switch Control System

This project provides a control system for radar switch relays using an Arduino microcontroller and Python control script.

## Features
- Control up to 4 relays via serial communication
- Real-time status monitoring
- JSON-based command interface
- Visual status display

## Hardware Requirements
- Arduino-compatible microcontroller
- 4-channel relay module
- Serial connection (USB or UART)

## Software Requirements
- Arduino IDE
- Python 3.x
- Required Python packages:
  - pyserial
  - json

## Installation

### Arduino Setup
1. Connect your Arduino to the relay module
2. Upload the `main.cpp` sketch to your Arduino
3. Note the COM port being used

### Python Setup
1. Install required packages:
   ```bash
   pip install pyserial
   ```
2. Update the `SERIAL_PORT` in `relay_control.py` with your Arduino's COM port

## Usage

### Basic Control
```python
python relay_control.py
```

### Command Format
- Turn on relay 1:
  ```json
  {"relays": {"relay1": 1}}
  ```
- Turn off relay 2:
  ```json
  {"relays": {"relay2": 0}}
  ```
- Get status:
  ```json
  {"command": "status"}
  ```

## Example Output
```
┌──────────────────────────────┐
│       Relay Status Board     │
├───────────────┬──────────────┤
│    Relay #    │    State     │
├───────────────┼──────────────┤
│ Relay 1       │ ● ON         │
│ Relay 2       │ ○ OFF        │
│ Relay 3       │ ● ON         │
│ Relay 4       │ ○ OFF        │
└───────────────┴──────────────┘
```

## License
MIT License - See LICENSE file for details

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
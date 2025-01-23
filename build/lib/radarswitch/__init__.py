import serial
import time
import json
from typing import Dict, Optional

class RadarSwitch:
    """Control and monitor radar switch relays"""
    
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 1.0):
        """
        Initialize the radar switch controller
        
        Args:
            port: Serial port name (e.g. 'COM25')
            baudrate: Baud rate for serial communication (default: 9600)
            timeout: Serial timeout in seconds (default: 1.0)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """Establish serial connection"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Allow Arduino to initialize
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to connect to {self.port}: {e}")

    def close(self):
        """Close serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def _clear_buffer(self):
        """Clear any pending data in the serial buffer"""
        while self.ser.in_waiting:
            self.ser.read(self.ser.in_waiting)

    def set_relay(self, relay_num: int, state: bool) -> bool:
        """
        Set relay state
        
        Args:
            relay_num: Relay number (1-4)
            state: True to turn on, False to turn off
            
        Returns:
            bool: True if command was sent successfully
        """
        if not 1 <= relay_num <= 4:
            raise ValueError("Relay number must be between 1 and 4")

        command = {
            "relays": {
                f"relay{relay_num}": int(state)
            }
        }
        
        try:
            self._clear_buffer()
            self.ser.write(json.dumps(command).encode('utf-8'))
            self.ser.write(b'\n')
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to send relay command: {e}")

    def get_relay(self, relay_num: int) -> bool:
        """
        Get the state of a specific relay
        
        Args:
            relay_num: Relay number (1-4)
            
        Returns:
            bool: True if relay is on, False if off
            
        Raises:
            ValueError: If relay number is invalid
            RuntimeError: If communication fails
        """
        if not 1 <= relay_num <= 4:
            raise ValueError("Relay number must be between 1 and 4")
            
        status = self.get_status()
        relay_key = f"relay{relay_num}"
        return bool(status.get(relay_key, False))

    def get_status(self) -> Dict[str, int]:
        """
        Get current relay status
        
        Returns:
            Dict[str, int]: Dictionary of relay states (e.g. {"relay1": 1})
        """
        try:
            self._clear_buffer()
            command = {"command": "status"}
            self.ser.write(json.dumps(command).encode('utf-8'))
            self.ser.write(b'\n')
            
            # Wait for response
            time.sleep(0.2)
            response_lines = []
            while self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    response_lines.append(line)
            
            # Parse response
            if response_lines:
                for line in reversed(response_lines):
                    if line.startswith('{') and line.endswith('}'):
                        try:
                            status = json.loads(line)
                            return status.get("status", {})
                        except json.JSONDecodeError:
                            continue
            return {}
        except Exception as e:
            raise RuntimeError(f"Failed to get relay status: {e}")

    def print_status(self, status: Optional[Dict[str, int]] = None):
        """
        Print formatted relay status
        
        Args:
            status: Optional status dictionary to print. If None, gets current status.
        """
        if status is None:
            status = self.get_status()
            
        if not status:
            print("No status received")
            return
        
        print("\n┌──────────────────────────────┐")
        print("│       Relay Status Board     │")
        print("├───────────────┬──────────────┤")
        print("│    Relay #    │    State     │")
        print("├───────────────┼──────────────┤")
        
        for relay, state in sorted(status.items()):
            relay_num = relay.replace("relay", "")
            state_str = "● ON " if state else "○ OFF"
            print(f"│ Relay {relay_num:<6} │ {state_str:<12} │")
        
        print("└───────────────┴──────────────┘")
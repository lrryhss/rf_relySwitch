import serial
import time
import json

# Configure serial port (update COM port as needed)
SERIAL_PORT = 'COM25'  # Change to your Arduino's COM port
BAUD_RATE = 9600

def clear_serial_buffer(ser):
    """Clear any pending data in the serial buffer"""
    while ser.in_waiting:
        ser.read(ser.in_waiting)

def send_relay_command(ser, relay_num, state):
    """Send JSON command to control a relay"""
    command = {
        "relays": {
            f"relay{relay_num}": int(state)
        }
    }
    
    try:
        # Clear buffer before sending
        clear_serial_buffer(ser)
        
        # Send command
        ser.write(json.dumps(command).encode('utf-8'))
        ser.write(b'\n')
        
        # Read Arduino response
        time.sleep(0.1)  # Allow time for Arduino to process
        while ser.in_waiting:
            response = ser.readline().decode('utf-8').strip()
            print(f"Arduino: {response}")
            
        print(f"Sent command: {command}")
    except Exception as e:
        print(f"Error communicating with Arduino: {e}")

def get_relay_status(ser):
    """Request and return current relay status"""
    try:
        # Clear buffer before sending
        clear_serial_buffer(ser)
        
        # Send status request
        command = {"command": "status"}
        json_command = json.dumps(command)
        ser.write(json_command.encode('utf-8'))
        ser.write(b'\n')
        
        # Debug print the sent command
        print(f"Sent status request: {json_command}")
        
        # Wait for response and collect all lines
        time.sleep(0.2)
        response_lines = []
        while ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                response_lines.append(line)
        
        # Try to parse the last line as JSON
        if response_lines:
            try:
                # Look for the actual JSON response (usually the last line)
                for line in reversed(response_lines):
                    if line.startswith('{') and line.endswith('}'):
                        status = json.loads(line)
                        return status.get("status", {})
                
                # If no valid JSON found, print debug info
                print(f"Could not find valid JSON in response: {response_lines}")
                return {}
            except json.JSONDecodeError:
                print(f"Invalid JSON response: {response_lines[-1]}")
                return {}
        return {}
    except Exception as e:
        print(f"Error getting relay status: {e}")
        return {}

def print_relay_status(status):
    """Print formatted relay status with visual indicators"""
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

if __name__ == "__main__":
    try:
        # Open serial connection once
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            # Wait for Arduino to initialize
            time.sleep(2)
            
            # Get initial status
            initial_status = get_relay_status(ser)
            print_relay_status(initial_status)
            
            # Cycle through all relays
            for relay in range(1, 5):
                print(f"\nTurning on relay {relay}")
                send_relay_command(ser, relay, True)  # Turn relay on
                time.sleep(2)  # Keep relay on for 2 seconds
                
                # Get current status
                current_status = get_relay_status(ser)
                print_relay_status(current_status)
                
            # Cycle through all relays
            for relay in range(1, 5):
                print(f"\nTurning off relay {relay}")
                send_relay_command(ser, relay, False)  # Turn relay off
                time.sleep(0.5)  # Short delay between relays
                
                # Get current status
                current_status = get_relay_status(ser)
                print_relay_status(current_status)
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
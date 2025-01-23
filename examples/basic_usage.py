from radarswitch import RadarSwitch

def main():
    # Example usage
    with RadarSwitch('COM25') as rs:
        # Print initial status
        rs.print_status()
        
        # Turn on relay 1
        rs.set_relay(1, True)
        
        # Check relay 1 state
        if rs.get_relay(1):
            print("Relay 1 is ON")
        else:
            print("Relay 1 is OFF")
            
        # Print updated status
        rs.print_status()
        
        # Turn off relay 1
        rs.set_relay(1, False)
        
        # Check relay 1 state
        if rs.get_relay(1):
            print("Relay 1 is ON")
        else:
            print("Relay 1 is OFF")
            
        # Print final status
        rs.print_status()

if __name__ == "__main__":
    main()
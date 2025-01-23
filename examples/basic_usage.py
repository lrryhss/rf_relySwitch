from radarswitch import RadarSwitch

def main():
    # Example usage
    with RadarSwitch('COM25') as rs:
        # Print initial status
        rs.print_status()
        
        # Turn on relay 1
        rs.set_relay(1, True)
        rs.print_status()
        
        # Turn off relay 1
        rs.set_relay(1, False)
        rs.print_status()

if __name__ == "__main__":
    main()
import sys
import serial
import readline

def main(port):
    # Configure the serial port
    serial_port = serial.Serial()
    serial_port.port = port
    serial_port.baudrate = 9600
    serial_port.parity = serial.PARITY_NONE
    serial_port.bytesize = serial.EIGHTBITS
    serial_port.stopbits = serial.STOPBITS_ONE
    serial_port.xonxoff = True
    serial_port.timeout = 1  # Set the timeout to 1 second

    # Initialize an empty list to store the command history
    history = []

    try:
        # Open the COM port
        serial_port.open()

        while True:
            # Read the command from keyboard input with history support
            tx_message = input("Enter a command (or 'quit' to exit): ")

            if tx_message.lower() == 'quit':
                break

            # Add the command to the history
            history.append(tx_message)

            # Send the command to the power supply
            serial_port.write(tx_message.encode() + b"\n")

            # Get the response
            rx_message = serial_port.readline().decode().strip()
            print("Response:", rx_message)

    except serial.SerialException as e:
        print("Error:", e)

    finally:
        # Close the COM port
        serial_port.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the serial port as a command-line argument.")
        print("Usage: python script_name.py <serial_port>")
        sys.exit(1)

    port = sys.argv[1]

    # Enable command history and tab completion
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')

    main(port)

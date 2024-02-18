import serial
import time

def send_command(ser, command):
    ser.write(command.encode())

# Change the port and baud rate based on your Arduino configuration
ser = serial.Serial('COM4', 9600, timeout=1)

try:
    while True:
        user_input = input("Enter 'd' to trigger dispensing: ")
        
        if user_input.lower() == 'd':
            send_command(ser, 'd')
            time.sleep(2)  # Adjust the delay to match the delay in your Arduino code

except KeyboardInterrupt:
    ser.close()
    print("Serial port closed.")

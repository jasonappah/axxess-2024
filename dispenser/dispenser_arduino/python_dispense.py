import serial
from secret import API_ENDPOINT

def send_command(ser, command):
    ser.write(command.encode())

# Change the port and baud rate based on your Arduino configuration
ser = serial.Serial('COM4', 9600, timeout=1)

try:
    while True:
        #TODO: Change the user input to the API response of number of pills to dispense
        user_input = input("Enter '#' to trigger dispensing: ")
        send_command(ser, user_input)
        #Wait until the user acknowledges the dispensing
        while ser.in_waiting == 0:
            pass
        ser.read()
        print("Dispensing acknowledged")
        #Send the dispensing event to the API server


except KeyboardInterrupt:
    ser.close()
    print("Serial port closed.")

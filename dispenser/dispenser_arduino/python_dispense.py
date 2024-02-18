import serial
from secret import API_ENDPOINT
import requests
import time

def send_command(ser, command):
    ser.write(command.encode())

# Change the port and baud rate based on your Arduino configuration
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)
try:
    while True:
        #TODO: Change the user input to the API response of number of pills to dispense
        endpoint = API_ENDPOINT + "/users/due_for_dispense"
        response = requests.get(endpoint)
        print(response.json())
        user_input = str(response.json())
        send_command(ser, user_input)
        print("send")
        #Wait until the user acknowledges the dispensing
        while ser.in_waiting == 0:
            pass
        ser.read()
        print("Dispensing acknowledged")
        #Send the dispensing event to the API server
        endpoint = API_ENDPOINT + "/users/consume"
        response = requests.get(endpoint)
        


except KeyboardInterrupt:
    ser.close()
    print("Serial port closed.")

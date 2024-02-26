import serial
from secret import API_ENDPOINT
import requests
import time

OFFLINE = True
USER_ID = 'SAMPLE_PATIENT'
def send_command(ser, command):
    ser.write(command.encode())

# Change the port and baud rate based on your Arduino configuration
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)

while True:
    #TODO: Change the user input to the API response of number of pills to dispense
    user_input = ""
    if OFFLINE:
        user_input = input("Enter the number of pills to dispense: ")
    else:
        endpoint = API_ENDPOINT + f"/users/{USER_ID}/due_for_dispense"
        response = requests.get(endpoint)
        if int(response.json()) == 0:
            time.sleep(1)
            continue
        user_input = str(response.json())
    send_command(ser, user_input)
    print("send")
    #Wait until the user acknowledges the dispensing
    while ser.in_waiting == 0:
        if ser.read() == b'1':
            break
        time.sleep(.5)
    
    print("Dispensing acknowledged")
    #Send the dispensing event to the API server
    endpoint = API_ENDPOINT + f"/users/{USER_ID}/consume"
    response = requests.get(endpoint)

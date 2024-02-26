
import tkinter as tk
from tkinter import PhotoImage
from AzureSpeech import recognize_from_microphone, text_to_speech
from secret import API_ENDPOINT
import requests
import json
import time

import os

USER_ID = 'SAMPLE_PATIENT'
TIME_BEFORE_CRY = 10 # 5 seconds

def send_command(ser, command):
    ser.write(command.encode())

script_dir = os.path.dirname(os.path.abspath(__file__))
emotion_folder_file_path = os.path.join(script_dir, "emotions/")

def get_biggest_image_dim():
    biggest_dim = 0
    for file in os.listdir(emotion_folder_file_path):
        if file.endswith(".png"):
            image = PhotoImage(file=emotion_folder_file_path + file)
            if image.width() > biggest_dim:
                biggest_dim = image.width()
            if image.height() > biggest_dim:
                biggest_dim = image.height()
    return biggest_dim


class Gia:
    def __init__(self, root) -> None:
        
        self.isConversing = False
        self.first_occurance_of_pill_time = None
        self.current_emotion = "smile"

        self.root = root
        self.root.title("Gia")
        self.root.geometry(str(get_biggest_image_dim()) + "x" + str(get_biggest_image_dim() + 50))
        #Make all the widgets contain in the root
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.resizable(False, False)

        self.image_label = tk.Label(root)
        self.image_label.pack()

        #Button to record audio
        self.record_button = tk.Button(root, text="Record", command=self.converse)
        #Make the button bigger
        self.record_button.config(height=4, width=40)
        #Make it Blue
        self.record_button.config(bg="red")
        self.record_button.pack()

        self.scheduler()

        self.change_emotion("smile")

    def scheduler(self):
        self.root.after(1000, self.check_if_pill_drink)


    def change_emotion(self, emotion):
        self.current_emotion = emotion
        self.image = PhotoImage(file=emotion_folder_file_path + emotion + ".png")
        self.image_label.config(image=self.image)
        self.image_label.image = self.image
        self.root.update()

    def converse(self):
        if self.isConversing:
            return
        prevEmotion = self.current_emotion

        self.isConversing = True
        #Change the button color to green
        self.record_button.config(bg="green")
        #Change the emotion to ear
        self.change_emotion("ear")
        #Record the audio
        text = recognize_from_microphone()
        print(text)
        #Change the mood to smile
        self.change_emotion("smile")
        #Send the text to API Server
        endpoint = API_ENDPOINT + f"/chat/message?=user_id={USER_ID}"
        data = {
            "chat_role": "user",
            "message": text
        }
        #Jsonify the data and send it to the server
        data = json.dumps(data)
        response = requests.post(endpoint, data=data)
        #Check if the response is successful
        print(response.status_code)

        message = response.json()["chat_message"]["message"]
        #Say the message
        text_to_speech(message)

        #Change the button color back to red
        self.record_button.config(bg="red")
        self.isConversing = False
        self.change_emotion(prevEmotion)

    def close(self):
        self.root.destroy()

    def check_if_pill_drink(self):
        if self.isConversing:
            return
        #Poll the server to see how many pill are dispensed
        # endpoint = API_ENDPOINT + "/pill/drink"
        # response = requests.get(endpoint)
        #Assume there are 2 pills in the dispenser
        endpoint = API_ENDPOINT + f"/users/{USER_ID}/due_for_dispense"
        response = requests.get(endpoint)
        self.pills_to_dispense = int(response.json())
        pills_to_dispense = self.pills_to_dispense
        print(pills_to_dispense)
        if pills_to_dispense <= 0:
            if self.first_occurance_of_pill_time:
                if self.current_emotion != "love":
                    self.change_emotion("love")
                    text_to_speech("I am happy that you took your pills")
                    #Wait for the audio to finish
                    time.sleep(2)
            self.root.after(1000, self.check_if_pill_drink)
            return

        if self.first_occurance_of_pill_time is None:
            print("Set first occurance of pill time to now")
            self.first_occurance_of_pill_time = time.time()

        elif self.first_occurance_of_pill_time and time.time() - self.first_occurance_of_pill_time > TIME_BEFORE_CRY:
            if self.current_emotion != "cry":
                self.change_emotion("cry")
                text_to_speech("You have not taken your pills, you should take them")
                #Wait for the audio to finish
                time.sleep(2)
        

        self.root.after(1000, self.check_if_pill_drink)

if __name__ == "__main__":
    root = tk.Tk()
    emotion = Gia(root)
    root.mainloop()
#define servo 8
#define led_r 4
#define led_y 5
#define led_g 6
#define button 7

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
bool ready_to_dispense = false;
int nums_pills = 0;

void setup() {
  myservo.attach(servo);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  pinMode(led_r, OUTPUT);
  pinMode(led_y, OUTPUT);
  pinMode(led_g, OUTPUT);
  pinMode(button, INPUT);

}

void dispense(){
  //Go really slow from 0 to 180 degrees
  for (int pos = 0; pos <= 180; pos += 1) {
    // in steps of 1 degree
    myservo.write(pos);
    delay(1);
  }
  delay(1000);
  //Go really slow from 180 to 0 degrees
  for (int pos = 180; pos >= 0; pos -= 1) {
    myservo.write(pos);
    delay(1);
  }
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    // Get numbers of pills from char
    nums_pills = command - '0';
    ready_to_dispense = true;
  }
  if (nums_pills <= 0) {
    digitalWrite(led_g, LOW);
    digitalWrite(led_y, LOW);
    digitalWrite(led_r, HIGH);
  }

  if (ready_to_dispense) {
    digitalWrite(led_g, HIGH);
    digitalWrite(led_y, LOW);
    digitalWrite(led_r, LOW);
  } else {
    digitalWrite(led_g, LOW);
    digitalWrite(led_y, LOW);
    digitalWrite(led_r, HIGH);
  }

  if (digitalRead(button) == HIGH && ready_to_dispense) {
    digitalWrite(led_g, LOW);
    digitalWrite(led_y, HIGH);
    digitalWrite(led_r, LOW);
    for (int i = 0; i < nums_pills; i++) {
      dispense();
    }
    nums_pills = 0;
    ready_to_dispense = false;
    // Send message to server
    Serial.println("dispensed");
  }



}

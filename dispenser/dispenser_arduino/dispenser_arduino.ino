#define servo 8
#define led_r 4
#define led_y 5
#define led_g 6
#define button 7

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
bool ready_to_dispense = false;

void setup() {
  myservo.attach(servo);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  pinMode(led_r, OUTPUT);
  pinMode(led_y, OUTPUT);
  pinMode(led_g, OUTPUT);
  pinMode(button, INPUT);
}

void dispense(){
  myservo.write(0);
  delay(100);
  myservo.write(45);
  delay(100);
  myservo.write(90);
  delay(100);
  myservo.write(135);
  delay(100);
  myservo.write(180);
  delay(1000);
  myservo.write(135);
  delay(100);
  myservo.write(90);
  delay(100);
  myservo.write(45);
  delay(100);
  myservo.write(0);
  delay(100);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == 'd') {
      ready_to_dispense = true;
    }
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
    dispense();
    ready_to_dispense = false;
  }



}

#include <Servo.h>
#include <SoftwareSerial.h>

//define Ultrasonic
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
#define srvout 4 //attach pin D4 Arduino to move servo

// defines variables
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
Servo servo;
int angle = 90;
SoftwareSerial BTSerial(8,9); // RX, TX - Bluetooth

void setup() {
  //Bluetooth:
  Serial.begin(115200);
  Serial.println("Arduino UP locally!");
  // set the data rate for the SoftwareSerial port
  BTSerial.begin(38400);
  BTSerial.println("*1Robot connected*");
  //Servo+ultrasonic:
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  servo.attach(srvout);
  servo.write(angle);
}
void loop() {
  /* if (mySerial.available()){  HOW Bluetooth read is made
   Serial.write(mySerial.read());
  }
  if (Serial.available()){ HOW BLUETOOTH WRITE IS MADE
   BTSerial.write(Serial.read());
  }*/
if (BTSerial.available()){                     // *** NEED TO check how to STOP CYCLE UPON DISCONNECTION.
  for(angle = 0; angle < 180; angle++)  
  {                                  
    // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
    // Displays the distance on the BTMonitor
    BTSerial.print("*1Distance: ");
    BTSerial.print(distance);
    BTSerial.print(" cm*");
    BTSerial.print("*2Angle: ");
    BTSerial.print(angle);
    BTSerial.println(" deg*");
    servo.write(angle);               
    delay(5);                   
  } 
  // now scan back from 180 to 0 degrees
  for(angle = 180; angle > 0; angle--)    
  {                                
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
    BTSerial.print("*1Distance: ");
    BTSerial.print(distance);
    BTSerial.print(" cm*");
    BTSerial.print("*2Angle: ");
    BTSerial.print(angle);
    BTSerial.println(" deg*");
    servo.write(angle);     
    delay(5);       
  } 
}
}

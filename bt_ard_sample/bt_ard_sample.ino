#include <SoftwareSerial.h>
SoftwareSerial mySerial(8,9); // RX, TX

void setup()
{
// Open serial communications and wait for port to open:
Serial.begin(115200);
Serial.println("Goodnight moon!");

// set the data rate for the SoftwareSerial port
mySerial.begin(115200);
mySerial.println("1_Hello, world");
}

void loop() // run over and over
{
if (mySerial.available())
Serial.write(mySerial.read());
if (Serial.available())
mySerial.write(Serial.read());
}

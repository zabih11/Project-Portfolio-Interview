#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>
#include <Servo.h>

int mode;
int Joint1Angle;
int Joint2Angle;
int Joint3Angle;
int Joint4Angle;
int Speed;

RF24 radio(7, 8); // CE,CSN
const byte address[6] = "00002";

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(10);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX);
  radio.stopListening();
}

void loop()
{

  if (Serial.available() > 0)
  {
    String message = Serial.readStringUntil('\n');
    int parts = sscanf(message.c_str(), "%d %d %d %d %d %d", &mode, &Joint1Angle, &Joint2Angle, &Joint3Angle, &Joint4Angle, &Speed);

    // Convert the values into a formatted string
    char txt[30]; // Adjust the size as per your requirements
    sprintf(txt, "%d %d %d %d %d %d", mode, Joint1Angle, Joint2Angle, Joint3Angle, Joint4Angle, Speed);

    // Send the string over radio
    radio.write(txt, sizeof(txt));
  }
  // const char txt[] = "Hello World";
  // radio.write(txt, sizeof(txt));
  delay(100);
}

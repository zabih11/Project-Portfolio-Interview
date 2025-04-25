#include <Adafruit_MotorShield.h>
#include <Servo.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61);

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
Adafruit_DCMotor *myMotor3 = AFMS.getMotor(3);
Adafruit_DCMotor *myMotor4 = AFMS.getMotor(4);

// Arm Servo pins
#define Joint1Pin 16
#define Joint2Pin 14
#define Joint3Pin 15
#define GripperPin 17
// Servo Objects
Servo Joint1;
Servo Joint2;
Servo Joint3;
Servo Gripper;
// Starting Joint Angles
int Joint1Angle = 90;   // Change 5 sets of angles
int Joint2Angle = 125;  // Change 5 sets of angles
int Joint3Angle = 145;  // Change 5 sets of angles
int Joint4Angle = 90;   // Change 5 sets of angles
int GripperOpen = 60;   // Open gripper; Need to tune value
int GripperClose = 120; // Close gripper; Need to tune value

// Joint Angle Offsets
int Joint1Offset = 7; // Your value may be different
int Joint2Offset = 0; // Your value may be different
int Joint3Offset = 5; // Your value may be different

// Motor Direction
int Circle_Dir;
int Square_Dir;
int Plus_Dir;
int Triangle_Dir;
int mode;
int Speed;

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(10);
  Joint1.attach(Joint1Pin);
  Joint2.attach(Joint2Pin);
  Joint3.attach(Joint3Pin);
  Gripper.attach(GripperPin);
  Joint1.write(Joint1Angle + Joint1Offset);
  Joint2.write(Joint2Angle + Joint2Offset);
  Joint3.write(Joint3Angle + Joint3Offset);
  Gripper.write(GripperOpen); // Open gripper

  if (!AFMS.begin())
  {
    while (1)
      ;
  }

  delay(1000); // 5 seconds before loop function
}

void loop()
{
  if (Serial.available() > 0)
  {
    String message = Serial.readStringUntil('\n'); // Read the message until a newline character is received
    // Split the message into individual parts
    if (message.length() <= 23)
    {
      int parts = sscanf(message.c_str(), "%d %d %d %d %d %d", &mode, &Joint1Angle, &Joint2Angle, &Joint3Angle, &Joint4Angle, &Speed);
      if (mode == 0)
      {
        Joint1.write(Joint1Angle + Joint1Offset);
        Joint2.write(Joint2Angle + Joint2Offset);
        Joint3.write(Joint3Angle + Joint3Offset);
        Gripper.write(Joint4Angle);
      }

      if (mode == 1)
      {
        Circle_Dir = Joint1Angle;
        Square_Dir = Joint2Angle;
        Plus_Dir = Joint3Angle;
        Triangle_Dir = Joint4Angle;

        if (Circle_Dir == 0)
        {
          myMotor3->setSpeed(Speed); // circle
          myMotor3->run(BACKWARD);
        }
        if (Circle_Dir == 1)
        {
          myMotor3->setSpeed(Speed); // circle
          myMotor3->run(FORWARD);
        }
        if (Circle_Dir == 2)
        {
          myMotor3->setSpeed(Speed); // circle
          myMotor3->run(RELEASE);
        }
        if (Square_Dir == 0)
        {
          myMotor2->setSpeed(Speed); // square
          myMotor2->run(BACKWARD);
        }
        if (Square_Dir == 1)
        {
          myMotor2->setSpeed(Speed); // square
          myMotor2->run(FORWARD);
        }
        if (Square_Dir == 2)
        {
          myMotor2->setSpeed(Speed); // square
          myMotor2->run(RELEASE);
        }
        if (Plus_Dir == 0)
        {
          myMotor4->setSpeed(Speed); // PLUS
          myMotor4->run(FORWARD);
        }
        if (Plus_Dir == 1)
        {
          myMotor4->setSpeed(Speed); // PLUS
          myMotor4->run(BACKWARD);
        }
        if (Plus_Dir == 2)
        {
          myMotor4->setSpeed(Speed); // PLUS
          myMotor4->run(RELEASE);
        }
        if (Triangle_Dir == 0)
        {
          myMotor1->setSpeed(Speed); // square
          myMotor1->run(FORWARD);
        }
        if (Triangle_Dir == 1)
        {
          myMotor1->setSpeed(Speed); // square
          myMotor1->run(BACKWARD);
        }
        if (Triangle_Dir == 2)
        {
          myMotor1->setSpeed(Speed); // square
          myMotor1->run(RELEASE);
        }
      }
    }
  }
  delay(10);
}

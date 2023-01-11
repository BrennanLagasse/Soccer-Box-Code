/******************************************************************************
 * This is the code frame for all arduinos, 1/4/2023
Hardware Hookup:
Mux Breakout ----------- Arduino
     S0 ------------------- 2
     S1 ------------------- 3
     S2 ------------------- 4
     Z -------------------- A0
    VCC ------------------- 5V
    GND ------------------- GND
    (VEE should be connected to GND)

The multiplexers independent I/O (Y0-Y7) can each be wired
up to a potentiometer or any other analog signal-producing
component.

Development environment specifics:
Arduino 1.6.9
SparkFun Multiplexer Breakout - 8-Channel(74HC4051) v10
(https://www.sparkfun.com/products/13906)
******************************************************************************/

// Pins
const int selectPins[3] = {2, 3, 4}; // S0~2, S1~3, S2~4
const int zInput = A0; // Connect common (Z) to A0 (analog input)

// Define piezoceramics
const int numPiezos = 8;
const float bounceTime = 0.25;

// Track when targets are hit to incorporate bounce
float hitTime [numPiezos] = {0, 0, 0, 0, 0, 0, 0, 0};

// Global minimum value to consider triggered
const int threshold = 300;

void setup() 
{
  Serial.begin(9600); // Initialize the serial port
  // Set up the select pins as outputs:
  for (int i=0; i<3; i++)
  {
    pinMode(selectPins[i], OUTPUT);
    digitalWrite(selectPins[i], HIGH);
  }
  pinMode(zInput, INPUT); // Set up Z as an input
}

void loop() 
{

  // Iterate through all pressure sensors
  // Bounce time of 0.25 seconds
  for(int i = 0; i < numPiezos; i++) {
    selectMuxPin(i);
    if((analogRead(zInput) > threshold) && (millis() - hitTime[i] > bounceTime*1000)) {
      Serial.println(i);
      hitTime[i] = millis();
    }
  }
}

// The selectMuxPin function sets the S0, S1, and S2 pins given a pin from 0-7
void selectMuxPin(byte pin)
{
  for (int i=0; i<3; i++)
  {
    if (pin & (1<<i))
      digitalWrite(selectPins[i], HIGH);
    else
      digitalWrite(selectPins[i], LOW);
  }
}

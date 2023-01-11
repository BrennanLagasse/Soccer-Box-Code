/******************************************************************************
 * Code frame for nanos including piezos and scoreboards
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

// Speaker Init ***************************************************************
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width,  in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// declare an SSD1306 display object connected to I2C
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Piezo Init *****************************************************************

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

// Setup **********************************************************************
void setup() {
  // Initialize the serial port
  Serial.begin(9600); 

  // Multiplexer **************************************************************

  // Set up the select pins as outputs:
  for (int i=0; i<3; i++)
  {
    pinMode(selectPins[i], OUTPUT);
    digitalWrite(selectPins[i], HIGH);
  }

  // Set the Z pin as input
  pinMode(zInput, INPUT); // Set up Z as an input

  // Scoreboard ***************************************************************

    // initialize OLED display with address 0x3C for 128x64
  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    while (true);
  }

  delay(2000);         // wait for initializing
  oled.clearDisplay(); // clear display

  oled.setTextSize(2);
  oled.setTextColor(WHITE);
  
  oled.setCursor(25, 0);
  oled.println("P1");
  
  oled.setCursor(85, 0);
  oled.println("P2");

  oled.setTextSize(3);

  oled.setCursor(20, 35);
  oled.println("01");

  oled.setCursor(80, 35);
  oled.println("15");
  oled.display();   
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

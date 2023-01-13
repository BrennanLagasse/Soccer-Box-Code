#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width,  in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// declare an SSD1306 display object connected to I2C
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Piezo Init ****************************************************************

// Pins
const int selectPins[3] = {2, 3, 4}; // S0~2, S1~3, S2~4
const int zInput = A0; // Connect common (Z) to A0 (analog input)


// Track when targets are hit to incorporate bounce
float hitTime [8] = {0, 0, 0, 0, 0, 0, 0, 0};

// Global minimum value to consider triggered
const int threshold = 300;

// Speaker *******************************************************************
//Lib to read SD card 
#include "SD.h"

//Lib to play auido
#include "TMRpcm.h" 

//SPI lib for SD card
#include "SPI.h"


// Used to be 4
#define SD_ChipSelectPin 10

TMRpcm music;

// Other *********************************************************************

int score1 = 0;
int score2 = 0;

// Store serial data
String msg;

// Setup *********************************************************************
void setup() {
  // Initialize the serial port
  Serial.begin(9600); 

  // Multiplexer *************************************************************

  // Set up the select pins as outputs:
  for (int i=0; i<3; i++)
  {
    pinMode(selectPins[i], OUTPUT);
    digitalWrite(selectPins[i], HIGH);
  }

  // Set the Z pin as input
  pinMode(zInput, INPUT); // Set up Z as an input

  // Scoreboard **************************************************************

    // initialize OLED display with address 0x3C for 128x64
  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    while (true);
  }

  // wait for initializing
  delay(2000);         

  setScoreboardDouble(0, 0); 

  // Speaker *****************************************************************
  music.speakerPin = 9; //Auido out on pin 9
  
  if (!SD.begin(SD_ChipSelectPin)) { 
    Serial.println("SD fail");
    return;
  }
  
  music.setVolume(4);    //   0 to 7. Set volume level
  
  music.quality(1);        //  Set 1 for 2x oversampling Set 0 for normal
}

void loop() 
{

  // Check for an update from the pi
  readSerialPort();

  if(msg != "") {
    // Check if it is a score message
    if(msg[0] == 'P') {
      // Check which player
      if(msg[1] == '0') {
        score1 = msg.substring(3).toInt();
        setScoreboardDouble(score1, score2);
      }
      else if(msg[1] == '1') {
        score2 = msg.substring(3).toInt();
        setScoreboardDouble(score1, score2);
      }
      else {
        oled.clearDisplay();

        oled.setTextSize(3);
        oled.setTextColor(WHITE);
      
        oled.setCursor(50, 0);
        oled.println(msg);
      }
    }
    else {
              
      if (msg == "red") {
        music.play("red.WAV");
      }
      else if (msg == "orange") {
        music.play("orange.WAV");  
      }
      else if (msg == "yellow") {
        music.play("yellow.WAV");
      }
      else if (msg == "green") {
        music.play("green.WAV");
      }
      else if (msg == "blue") {
        music.play("blue.WAV");
      }
      else if (msg == "purple") {
        music.play("purple.WAV");
      }
      else if (msg == "pink") {
        music.play("pink.WAV");
      }
      else if (msg == "white") {
        music.play("white.WAV");
      }
      else if(msg == "end\n") {
        music.play("end.WAV");
      }
      else if(msg == "end") {
        music.play("end.WAV");
        delay(3000);
        music.play("end.WAV");
      }
    }
  }

  // Iterate through all pressure sensors
  // Bounce time of 0.25 seconds
  for(int i = 0; i < 8; i++) {
    selectMuxPin(i);
    if((analogRead(zInput) > threshold) && (millis() - hitTime[i] > 275)) {
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

// The readSerialPort() function checks if there are any messages from the pi
void readSerialPort() {
  msg = "";
  if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
      msg += (char) Serial.read();
    }
    Serial.flush();
  }
}

// The setScoreSingle(int s1) prints the score for a single player game
// String s1 is the score of player1
void setScoreboardSingle(int s1) {
  oled.clearDisplay();

  oled.setTextSize(2);
  oled.setTextColor(WHITE);

  oled.setCursor(50, 0);
  oled.println("P1");

  oled.setTextSize(3);

  oled.setCursor(20, 35);
  oled.println(s1);

  oled.display(); 
}

// The setScoreDouble(int s1, int s2) prints the scores for a two player game
// String s1 is the score of player1
// String s2 is the score of player2
void setScoreboardDouble(int s1, int s2) {
  oled.clearDisplay();

  oled.setTextSize(2);
  oled.setTextColor(WHITE);

  oled.setCursor(25, 0);
  oled.println("P1");

  oled.setCursor(85, 0);
  oled.println("P2");

  oled.setTextSize(3);

  oled.setCursor(20, 35);
  oled.println(String(s1));

  oled.setCursor(80, 35);
  oled.println(String(s2));
  oled.display();  
}
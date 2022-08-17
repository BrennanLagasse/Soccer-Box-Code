// Code for the arduino for event management for:
// Piezoceramics (Serial Output)
// Speaker (Serial Input)
// Scoreboard (Serial Input)

// Note: this code gives a lot of warnings (red) when it downloads, but those are just technical warnings about syntax that do not apply. Disregard the warnings


//Lib to read SD card 
#include "SD.h"

//Lib to play auido
#include "TMRpcm.h" 

//SPI lib for SD card
#include "SPI.h"

// Define piezoceramics
const int numPiezos = 8;
const int piezoPin [numPiezos] = {A0, A1, A2, A3, A4, A5, A6, A7};
const float bounceTime = 0.25;

// Track when targets are hit to incorporate bounce
float hitTime [numPiezos] = {0, 0, 0, 0, 0, 0, 0, 0};

// Global minimum value to consider triggered
const int threshold = 300;

// Pin for sd card
#define SD_ChipSelectPin 4

int vol = 5;

TMRpcm music;

void setup(){

  // Set up all of the piezoceramics as analog inputs
  for(int i = 0; i < numPiezos; i++) {
    pinMode(piezoPin[i], INPUT);
  }

  // Define audio output pin
  music.speakerPin = 4;
  
  Serial.begin(9600);
  
  if (!SD.begin(SD_ChipSelectPin)) { 
    Serial.println("SD fail");
    return;
  }

  music.setVolume(vol);

  // 1 is higher quality, 0 is lower quality
  music.quality(1);
}


void loop() { 

  // Iterate through all pressure sensors
  // If a single readout exceeds the threshold, mark the target as triggered (max pool testing indicated high false-positive outliers are extremely rare)
  // Bounce time of 0.25 seconds
  for(int i = 0; i < numPiezos; i++) {
    if((analogRead(piezoPin[i]) > threshold) && (millis() - hitTime[i] > bounceTime*1000)) {
      Serial.println(i);
      hitTime[i] = millis();
    }
  }

  String content = "";
  char character;

  // Read any incoming values
  while(Serial.available()) {
    character = Serial.read();
    content.concat(character);
    delay(10);
  }
        
  if (content == "red\n") {
    music.setVolume(vol);
    Serial.println("yay");
    music.play("red.WAV");
  }
  else if (content == "orange\n") {
    music.setVolume(vol);
    Serial.println("orange");
    music.play("orange.WAV");  
  }
  else if (content == "yellow\n") {
    music.setVolume(vol);
    Serial.println("yellow");
    music.play("yellow.WAV");
  }
  else if (content == "green\n") {
    music.setVolume(vol);
    Serial.println("green");
    music.play("green.WAV");
  }
  else if (content == "blue\n") {
    music.setVolume(vol);
    Serial.println("blue");
    music.play("blue.WAV");
  }
  else if (content == "purple\n") {
    music.setVolume(vol);
    Serial.println("purple");
    music.play("purple.WAV");
  }
  else if (content == "pink\n") {
    music.setVolume(vol);
    Serial.println("pink");
    music.play("pink.WAV");
  }
  else if (content == "white\n") {
    music.setVolume(vol);
    Serial.println("white");
    music.play("white.WAV");
  }
  else if (content == "miss\n") {
    music.setVolume(vol);
    Serial.println("miss");
    music.play("miss.WAV");
  }
  else if (content == "end\n") {
    music.setVolume(vol);
    Serial.println("end");
    music.play("end.WAV");
  }
  else if (content.charAt(0) == "P") {
    // Handles all inputs related to scores
    int player = content.substring(0, 1).toInt();
    int score = content.substring(3).toInt();

    print("CHANGE SCOREBOARD HERE")
  }
  


}
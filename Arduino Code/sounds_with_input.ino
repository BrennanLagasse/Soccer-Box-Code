//Lib to read SD card 
#include "SD.h"

//Lib to play auido
#include "TMRpcm.h" 

//SPI lib for SD card
#include "SPI.h"


#define SD_ChipSelectPin 4

TMRpcm music;

void setup(){
  
  music.speakerPin = 9; //Auido out on pin 9
  
  Serial.begin(9600); //Serial Com for debugging 
  
  if (!SD.begin(SD_ChipSelectPin)) { 
    Serial.println("SD fail");
    return;
  }
  
  music.setVolume(5);    //   0 to 7. Set volume level
  
  music.quality(1);        //  Set 1 for 2x oversampling Set 0 for normal
}


void loop() { 

    String content = "";
  char character;

      
  while(Serial.available()) {
    character = Serial.read();
    content.concat(character);
    delay(10);
  }
        
  if (content == "red\n") {
    Serial.println("yay");
    music.play("red.WAV");
  }
  else if (content == "orange\n") {
    Serial.println("orange");
    music.play("orange.WAV");  
  }
  else if (content == "yellow\n") {
    Serial.println("yellow");
    music.play("yellow.WAV");
  }
  else if (content == "green\n") {
    Serial.println("green");
    music.play("green.WAV");
  }
  else if (content == "blue\n") {
    Serial.println("blue");
    music.play("blue.WAV");
  }
  else if (content == "purple\n") {
    Serial.println("purple");
    music.play("purple.WAV");
  }
  else if (content == "pink\n") {
    Serial.println("pink");
    music.play("pink.WAV");
  }
  else if (content == "white\n") {
    Serial.println("white");
    music.play("white.WAV");
  }


}

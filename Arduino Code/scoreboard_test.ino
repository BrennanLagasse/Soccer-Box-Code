/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-oled
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width,  in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// declare an SSD1306 display object connected to I2C
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(9600);

  // initialize OLED display with address 0x3C for 128x64
  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    while (true);
  }

  delay(2000);         // wait for initializing
  oled.clearDisplay(); // clear display

  //oled.textSize(x) changes the text size
  //oled.setCursor(x, y) determines the position to write in
  //oled.clearDisplay() clears display
  //oled.display shows new display
  //oled.println("text") displays test at given position

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

void loop() {
}

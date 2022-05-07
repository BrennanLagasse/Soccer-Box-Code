// Title:     Piezo Event Handler
// Purpose:   Sends messages via serial communication when targets are triggered
// Structure: Simeltaneously check all 7 piezoceramics for a hit and report back with a max pool algorithm

// Define piezoceramics
const int numPiezos = 8;
const int piezoPin [numPiezos] = {A0, A1, A2, A3, A4, A5, A6, A7};
const float bounceTime = 0.25;

// Track when targets are hit to incorporate bounce
float hitTime [numPiezos] = {0, 0, 0, 0, 0, 0, 0, 0};

// Global minimum value to consider triggered
const int threshold = 300;

void setup() {
  // Set up all of the piezoceramics as analog inputs
  for(int i = 0; i < numPiezos; i++) {
    pinMode(piezoPin[i], INPUT);
  }

  // Start Serial - must by the same frequency for Pi and Arduino (9600)
  Serial.begin(9600);
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
}

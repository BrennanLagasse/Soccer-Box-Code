// Title:     Piezo Event Handler
// Purpose:   Sends messages via serial communication when targets are triggered
// Structure: Averages piezo values over 3 trials and compares to a set threshold. This methodology should discount rapid spikes in electricity

// Define piezoceramics
const int numPiezos = 8;
const int piezoPin [numPiezos] = {A0, A1, A2, A3, A4, A5, A6, A7};

// Track data on piezoceramics
int piezoVal [numPiezos][4] = {{0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}};

// Variable target thresholds as a potential solution
const int thresholds [numPiezos] = {50, 50, 50, 50, 50, 50, 50, 50};

void setup() {
  // Set up all of the piezoceramics as analog inputs
  for(int i = 0; i < numPiezos; i++) {
    pinMode(piezoPin[i], INPUT);
  }

  // Start Serial - must by the same frequency for Pi and Arduino (9600)
  Serial.begin(9600);
}

int amax = 0;

void loop() {
  int m = millis();

  // Iterate through all pressure sensors
  //If the average value of a sensor over three checks is greater than the threshold, message that the target has been hit.
  for(int i = 0; i < 3600; i++) {
    int a = analogRead(piezoPin[5]);

    // Good range: idle < 100, active > 150

    // Replaced and Good (7/8)
    // 0, 1, 2, 3, 5, 6, 7

    // Missing (1/8)
    // 4 
    
   
    if(a > amax) {
      amax = a;
    }
  }
  Serial.println(amax);
  amax = 0;
}

void averageCheck(int average) {
  if(average > 20) {
    Serial.print(average);
  }
}

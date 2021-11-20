// Title:     Piezo Event Handler
// Purpose:   Sends messages via serial communication when targets are triggered
// Structure: Averages piezo values over 3 trials and compares to a set threshold. This methodology should discount rapid spikes in electricity

// Define piezoceramics
const int numPiezos = 8;
const int piezoPin [numPiezos] = {A0, A1, A2, A3, A4, A5, A6, A7};

// Track data on piezoceramics
int piezoVal [numPiezos][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}};

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

void loop() {
  int m = millis();

  // Iterate through all pressure sensors
  //If the average value of a sensor over three checks is greater than the threshold, message that the target has been hit.
  for(int i = 0; i < numPiezos; i++) {
    
    // Shift values over to clear space and delete the oldest value
    piezoVal[i][2] = piezoVal[i][1];
    piezoVal[i][1] = piezoVal[i][0];
    
    // Read new value
    piezoVal[i][0] = analogRead(piezoPin[i]);

    // Find the average over the past three checks
    double piezoAverage = (piezoVal[i][0] + piezoVal[i][1] + piezoVal[i][2]) / 3.0;

    // Determines if the piezoceramic value is above the threshold
    if(piezoAverage > thresholds[i]) {
      // Send the message
      Serial.println(i);
    }
  }
}

void averageCheck(int average) {
  if(average > 20) {
    Serial.print(average);
  }
}
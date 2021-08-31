const int numPiezos = 6;
const int piezoPin [numPiezos] = {A0, A1, A2, A3, A4, A5};
const int ledPin [numPiezos] = {2, 4, 7, 8, 12, 13};
int piezoVal [numPiezos] = {0, 0, 0, 0, 0, 0};
int triggerTime [numPiezos] = {0, 0, 0, 0, 0, 0};
bool piezosTriggered [numPiezos] = {false, false, false, false, false, false};

void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < numPiezos; i++) {
    pinMode(piezoPin[i], INPUT);
  }
  for(int i = 0; i < numPiezos; i++) {
    pinMode(ledPin[i], OUTPUT);
  }

  // Ensure serial frequency is the same for the pi
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  const int threshold = 75;
  const int bounce = 100;
  int m = millis();

  for(int i = 0; i < numPiezos; i++) {
    // Read value
    piezoVal[i] = analogRead(piezoPin[i]);

    // Return if passes threshold
    if(piezoVal[i] > threshold) {
      // Set state to triggered and send on message
      if(piezosTriggered[i] == false) {
        sendData(i);
        piezosTriggered[i] = true;
      }

      // Update timer
      triggerTime[i] = m;

      // Turn on LED
      digitalWrite(ledPin[i], HIGH);  
    }
    else if(piezosTriggered[i] && m - triggerTime[i] > bounce) {
      // Turn off LED
      digitalWrite(ledPin[i], LOW);

      // Set state to not triggered
      piezosTriggered[i] = false;
    }
    
  }
  
}

void sendData(int pin) {
  Serial.println(pin);
}
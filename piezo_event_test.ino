const int numPiezos = 3;
const int piezoPin [numPiezos] = {A0, A1, A2};
const int ledPin [numPiezos] = {2, 4, 7};
int piezoVal [numPiezos] = {0, 0, 0};
int triggerTime [numPiezos] = {0, 0, 0};

void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < numPiezos; i++) {
    pinMode(piezoPin[i], INPUT);
  }
  for(int i = 0; i < numPiezos; i++) {
    pinMode(ledPin[i], OUTPUT);
  }
  
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  const int threshold = 100;
  const int bounce = 100;
  int m = millis();

  for(int i = 0; i < numPiezos; i++) {
    // Read value
    piezoVal[i] = analogRead(piezoPin[i]);

    // Return if passes threshold
    if(piezoVal[i] > threshold) {
      Serial.println(i);
      triggerTime[i] = m;
      digitalWrite(ledPin[i], HIGH);  
    }
    else if(m - triggerTime[i] > bounce) {
      digitalWrite(ledPin[i], LOW);
    }
    
  }
  
}

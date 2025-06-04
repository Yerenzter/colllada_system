/*
* [PROJECT]: COLLISION DETECTOR SYSTEM
* CSJUH800P(L) 
*/

// DIGITAL PIN CONSTANTS
const int TRIG_PIN1 = 5;
const int ECHO_PIN1 = 6;
const int TRIG_PIN2 = 9;
const int ECHO_PIN2 = 10;

// LED PIN CONSTANTS
const int SAFE_ZONE_PIN = 2;
const int WARNING_ZONE_PIN = 3;
const int DANGER_ZONE_PIN = 4;

// INIITIALIZE ALL MODULES/COMPONENTS AND PINS.
void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN1, OUTPUT);
  pinMode(TRIG_PIN2, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(ECHO_PIN2, INPUT);

  pinMode(SAFE_ZONE_PIN, OUTPUT);
  pinMode(WARNING_ZONE_PIN, OUTPUT);
  pinMode(DANGER_ZONE_PIN, OUTPUT);
}


// DO SOMETHING IN EVERY TIME OR UPDATE THE STATES.
void loop() {
  long time1, time2, distance1, distance2;


  // SENSOR 1
  digitalWrite(TRIG_PIN1, LOW);
  delayMicroseconds(2);
  
  digitalWrite(TRIG_PIN1, HIGH);
  delayMicroseconds(5);

  digitalWrite(TRIG_PIN1, LOW);

  // SENSOR 2
  digitalWrite(TRIG_PIN2, LOW);
  delayMicroseconds(2);
  
  digitalWrite(TRIG_PIN2, HIGH);
  delayMicroseconds(5);

  digitalWrite(TRIG_PIN2, LOW);
  
  time1 = pulseIn(ECHO_PIN1, HIGH);
  time2 = pulseIn(ECHO_PIN2, HIGH);

  distance1 = (time1 * 0.0343) / 2;
  distance2 = (time2 * 0.0343) / 2;

  Serial.print("Front: ");
  Serial.print(centimeterToMeter(distance1));
  Serial.println(" m");

  Serial.print("Back: ");
  Serial.print(centimeterToMeter(distance2));
  Serial.println(" m");


  // PROXIMITY SIGNAL LOGIC FOR DISTANCE 1.
  if(4.0 < centimeterToMeter(distance1)) {
    TRIGGER_SAFE_ZONE(HIGH);
    return;
  }

  if(2.0 <= centimeterToMeter(distance1) > 4.0) {
    TRIGGER_WARNING_ZONE(HIGH);
    return;
  }

  if(centimeterToMeter(distance1) > 2.0) {
    TRIGGER_DANGER_ZONE(HIGH);
    return;
  }

  TRIGGER_SAFE_ZONE(LOW);
  TRIGGER_WARNING_ZONE(LOW);
  TRIGGER_DANGER_ZONE(LOW);

  delay(100);
}

// SOME USEFUL FUNCTIONS/METHODS...I GUESS...
float centimeterToMeter(float distance) {
  return distance / 100;
}

void TRIGGER_SAFE_ZONE(uint8_t state) {
  digitalWrite(SAFE_ZONE_PIN, state);
}

void TRIGGER_WARNING_ZONE(uint8_t state) {
  digitalWrite(WARNING_ZONE_PIN, state);
}

void TRIGGER_DANGER_ZONE(uint8_t state) {
  digitalWrite(DANGER_ZONE_PIN, state);
}
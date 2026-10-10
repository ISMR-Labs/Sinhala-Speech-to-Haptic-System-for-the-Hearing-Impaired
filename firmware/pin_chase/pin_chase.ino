// Turns on each pin one at a time, in order, on power-up (then repeats).
// Target: ESP32-S3 (GPIO 45-48 only exist on the S3).

const int PINS[] = {14, 13, 12, 11, 10, 9, 46, 3, 8, 18, 20, 47, 48, 45, 40, 41, 42, 2, 1, 19};
const int NUM_PINS = sizeof(PINS) / sizeof(PINS[0]);
const int ON_TIME_MS = 500;

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < NUM_PINS; i++) {
    pinMode(PINS[i], OUTPUT);
    digitalWrite(PINS[i], LOW);
  }
}

void loop() {
  for (int i = 0; i < NUM_PINS; i++) {
    digitalWrite(PINS[i], HIGH);
    Serial.printf("GPIO %d ON\n", PINS[i]);
    delay(ON_TIME_MS);
    digitalWrite(PINS[i], LOW);
  }
}

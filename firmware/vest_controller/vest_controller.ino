// Vest controller: drives 18 vibration-motor modules from an ESP32-S3 and plays
// frame sequences received over Wi-Fi (HTTP) or the USB serial port.
//
// Board: "ESP32S3 Dev Module" (esp32:esp32:esp32s3), Arduino-ESP32 core 3.x.
// Modules: 3-pin vibration motor modules (VCC, GND, IN). IN is driven directly by a GPIO;
// the module's own transistor switches the coin motor. Motors are powered from 5 V, not
// from the GPIO.
//
// Wire protocol (same over HTTP POST /play body and over serial, one command per line):
//   F <idx,idx,...> <ms> <level>;F <idx> <ms> <level>;...     play a sequence of frames
//   G <gap_ms>                                                gap between frames (default 80)
//   S                                                         stop
//   T                                                         test: chase through all motors
//   ?                                                         status
// idx = 0..17 (0-8 front, 9-17 back), level = 0..255 (software PWM, 100 Hz).
// Example word: "F 4 200 255;F 13 200 255"

#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include "secrets.h"   // WIFI_SSID, WIFI_PASS

static const int NUM_MOTORS = 18;
// Order follows the harness as built: first 18 of the 20 chase pins. GPIO 1 and 19 are spare.
static const int MOTOR_PIN[NUM_MOTORS] = {14, 13, 12, 11, 10, 9, 46, 3, 8, 18, 20, 47, 48, 45, 40, 41, 42, 2};
static const int LED_PIN = 38;           // on-board RGB/LED pin on most S3 devkits; harmless if absent
static const int MAX_FRAMES = 32;
static const uint32_t PWM_PERIOD_US = 10000;   // 100 Hz software PWM

struct Frame { uint32_t mask; uint16_t ms; uint8_t level; };

static Frame seq[MAX_FRAMES];
static int seqLen = 0, seqPos = -1;
static uint16_t gapMs = 80;
static bool inGap = false;
static uint32_t stepStart = 0;
static uint32_t curMask = 0;
static uint8_t curLevel = 0;
static uint32_t played = 0;

WebServer server(80);

// ---------------------------------------------------------------- output
static void applyOutputs() {
  // software PWM: on for level/255 of each 10 ms period
  uint32_t phase = micros() % PWM_PERIOD_US;
  bool on = phase < (uint32_t)curLevel * PWM_PERIOD_US / 255;
  for (int i = 0; i < NUM_MOTORS; i++) {
    bool want = on && (curMask & (1u << i));
    digitalWrite(MOTOR_PIN[i], want ? HIGH : LOW);
  }
}

static void allOff() {
  curMask = 0; curLevel = 0;
  for (int i = 0; i < NUM_MOTORS; i++) digitalWrite(MOTOR_PIN[i], LOW);
}

static void startFrame(int i) {
  seqPos = i; inGap = false; stepStart = millis();
  curMask = seq[i].mask; curLevel = seq[i].level;
  digitalWrite(LED_PIN, HIGH);
}

static void stopAll() { seqLen = 0; seqPos = -1; allOff(); digitalWrite(LED_PIN, LOW); }

static void tickPlayer() {
  if (seqPos < 0) return;
  uint32_t now = millis();
  if (!inGap) {
    if (now - stepStart >= seq[seqPos].ms) {
      allOff(); digitalWrite(LED_PIN, LOW);
      inGap = true; stepStart = now;
    }
  } else if (now - stepStart >= gapMs) {
    if (seqPos + 1 < seqLen) startFrame(seqPos + 1);
    else { seqPos = -1; seqLen = 0; played++; }
  }
  applyOutputs();
}

// ---------------------------------------------------------------- protocol
static String handleCommand(String line) {
  line.trim();
  if (line.length() == 0) return "ERR empty";
  char c = line.charAt(0);
  if (c == 'S') { stopAll(); return "OK stopped"; }
  if (c == '?') {
    return String("OK motors=") + NUM_MOTORS + " playing=" + (seqPos >= 0 ? "1" : "0") +
           " played=" + played + " gap=" + gapMs + " ip=" + WiFi.localIP().toString();
  }
  if (c == 'T') {
    seqLen = 0;
    for (int i = 0; i < NUM_MOTORS && seqLen < MAX_FRAMES; i++) seq[seqLen++] = {1u << i, 250, 255};
    startFrame(0);
    return "OK chase";
  }
  if (c == 'G') { gapMs = line.substring(1).toInt(); return String("OK gap=") + gapMs; }

  // frame list: "F idx,idx ms level;F ..."  (a leading "G n;" is also accepted)
  Frame tmp[MAX_FRAMES]; int n = 0;
  int start = 0;
  while (start < (int)line.length()) {
    int semi = line.indexOf(';', start);
    if (semi < 0) semi = line.length();
    String part = line.substring(start, semi); part.trim();
    start = semi + 1;
    if (part.length() == 0) continue;
    if (part.charAt(0) == 'G') { gapMs = part.substring(1).toInt(); continue; }
    if (part.charAt(0) != 'F') return "ERR bad token: " + part;
    if (n >= MAX_FRAMES) return "ERR too many frames";
    // tokens after 'F': idxlist ms level
    part = part.substring(1); part.trim();
    int sp1 = part.indexOf(' ');
    if (sp1 < 0) return "ERR frame needs 'idx ms level'";
    String idxs = part.substring(0, sp1);
    String rest = part.substring(sp1 + 1); rest.trim();
    int sp2 = rest.indexOf(' ');
    uint16_t ms = (sp2 < 0 ? rest : rest.substring(0, sp2)).toInt();
    uint8_t level = sp2 < 0 ? 255 : (uint8_t)constrain(rest.substring(sp2 + 1).toInt(), 0, 255);
    uint32_t mask = 0;
    int p = 0;
    while (p < (int)idxs.length()) {
      int comma = idxs.indexOf(',', p);
      if (comma < 0) comma = idxs.length();
      int idx = idxs.substring(p, comma).toInt();
      if (idx < 0 || idx >= NUM_MOTORS) return "ERR motor index out of range";
      mask |= 1u << idx;
      p = comma + 1;
    }
    if (ms == 0) ms = 200;
    tmp[n++] = {mask, ms, level};
  }
  if (n == 0) return "ERR no frames";
  stopAll();
  for (int i = 0; i < n; i++) seq[i] = tmp[i];
  seqLen = n;
  startFrame(0);
  return String("OK frames=") + n;
}

// ---------------------------------------------------------------- HTTP
static void httpStatus() { server.send(200, "text/plain", handleCommand("?")); }
static void httpPlay() {
  String body = server.hasArg("plain") ? server.arg("plain") : "";
  String r = handleCommand(body);
  server.send(r.startsWith("OK") ? 200 : 400, "text/plain", r);
}
static void httpStop() { server.send(200, "text/plain", handleCommand("S")); }
static void httpTest() { server.send(200, "text/plain", handleCommand("T")); }

// ---------------------------------------------------------------- setup / loop
void setup() {
  Serial.begin(115200);
  for (int i = 0; i < NUM_MOTORS; i++) { pinMode(MOTOR_PIN[i], OUTPUT); digitalWrite(MOTOR_PIN[i], LOW); }
  pinMode(LED_PIN, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.setHostname("vest");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("wifi");
  for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) { delay(250); Serial.print("."); }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("ip "); Serial.println(WiFi.localIP());
    if (MDNS.begin("vest")) Serial.println("mdns vest.local");
  } else {
    Serial.println("wifi failed; serial only");
  }
  server.on("/", HTTP_GET, httpStatus);
  server.on("/status", HTTP_GET, httpStatus);
  server.on("/play", HTTP_POST, httpPlay);
  server.on("/stop", HTTP_POST, httpStop);
  server.on("/test", HTTP_POST, httpTest);
  server.begin();
  Serial.println("ready: F idx,idx ms level;...  | S | T | ? | G ms");
}

void loop() {
  server.handleClient();
  tickPlayer();
  static String buf;
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n' || ch == '\r') {
      if (buf.length()) { Serial.println(handleCommand(buf)); buf = ""; }
    } else if (buf.length() < 1024) {
      buf += ch;
    }
  }
}

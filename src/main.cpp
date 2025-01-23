#include <Arduino.h>
#include <ArduinoJson.h>

// Relay pin definitions
const int RELAY_PINS[] = {2, 3, 4, 5};  // Pins for 4 relays
const int NUM_RELAYS = 4;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize relay pins as outputs
  for (int i = 0; i < NUM_RELAYS; i++) {
    pinMode(RELAY_PINS[i], OUTPUT);
    digitalWrite(RELAY_PINS[i], LOW);  // Start with all relays off (active LOW)
    Serial.print("Initialized relay ");
    Serial.print(i + 1);
    Serial.print(" on pin ");
    Serial.println(RELAY_PINS[i]);
  }
  
  // Initial status message
  Serial.println("Relay Control Program Started");
}

String getRelayStatus() {
  StaticJsonDocument<200> doc;
  JsonObject status = doc.createNestedObject("status");
  
  for (int i = 0; i < NUM_RELAYS; i++) {
    String relayKey = "relay" + String(i + 1);
    // Read pin state and invert for active LOW logic
    int state = digitalRead(RELAY_PINS[i]) == LOW ? 1 : 0;
    status[relayKey] = state;
  }
  
  String output;
  serializeJson(doc, output);
  return output;
}

void processCommand(const char* json) {
  Serial.print("Received JSON: ");
  Serial.println(json);
  
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, json);
  
  if (error) {
    Serial.print("JSON Error: ");
    Serial.println(error.c_str());
    return;
  }

  // Debug print parsed JSON
  Serial.println("Parsed JSON:");
  serializeJsonPretty(doc, Serial);
  Serial.println();

  // Handle status request
  if (doc.containsKey("command") && strcmp(doc["command"], "status") == 0) {
    String status = getRelayStatus();
    Serial.println(status);
    return;
  }

  // Handle both JSON formats
  JsonObject relays = doc.as<JsonObject>();
  if (doc.containsKey("relays")) {
    // Format: {"relays": {"relay1": 1}}
    relays = doc["relays"].as<JsonObject>();
  }

  for (int i = 0; i < NUM_RELAYS; i++) {
    String relayKey = "relay" + String(i + 1);
    if (relays.containsKey(relayKey)) {
      int state = relays[relayKey];
      Serial.print("Setting relay ");
      Serial.print(i + 1);
      Serial.print(" to ");
      Serial.println(state ? "ON" : "OFF");
      
      // Invert logic for active LOW relays
      digitalWrite(RELAY_PINS[i], state ? HIGH : LOW);
      
      // Verify pin state
      int actualState = digitalRead(RELAY_PINS[i]);
      Serial.print("Actual pin state: ");
      Serial.println(actualState == LOW ? "LOW (ON)" : "HIGH (OFF)");
    }
  }
}

void loop() {
  // Check for incoming serial data
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    processCommand(input.c_str());
  }
}
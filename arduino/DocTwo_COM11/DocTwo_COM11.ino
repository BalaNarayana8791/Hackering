#include <Wire.h>
#include "MAX30105.h"
#include <Adafruit_MLX90614.h>
#include <SSD1306Ascii.h>
#include <SSD1306AsciiWire.h>
#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

// Pins for DFPlayer Mini
SoftwareSerial mySoftwareSerial(10, 11); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

#define OLED_I2C_ADDRESS 0x3C
SSD1306AsciiWire display;
MAX30105 particleSensor;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

// Vitals
int bpm = 0;
int spo2 = 0;
float temp = 0.0;
bool fingerDetected = false;
unsigned long lastUpdate = 0;
unsigned long lastAlertTime = 0; // Cooldown for emergency alert
int simulationTick = 0;         // Cycle counter for simulation

void setup() {
  Serial.begin(115200);
  mySoftwareSerial.begin(9600); // DFPlayer communicates at 9600
  Wire.begin();
  Wire.setClock(400000L);

  display.begin(&Adafruit128x64, OLED_I2C_ADDRESS);
  display.setFont(System5x7);
  display.clear();
  display.println(F("Agentic-Med"));

  // Start DFPlayer
  if (!myDFPlayer.begin(mySoftwareSerial)) {
    display.println(F("DFP Fail"));
  } else {
    myDFPlayer.volume(25); // Set volume (0-30)
    myDFPlayer.play(1); // Play '0001.mp3' (Welcome Message)
    display.println(F("DFPlayer Ok"));
  }

  if (!mlx.begin()) {
    display.println(F("MLX90614 Fail"));
  } else {
    display.println(F("MLX90614 Ok"));
  }

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    display.println(F("MAX30105 Fail")); 
  } else {
    particleSensor.setup(); 
    display.println(F("MAX30105 Ok"));
  }

  delay(2000);
  display.clear();
  updateOLED(); 
  
  // Seed random with noise from an analog pin
  randomSeed(analogRead(0));
}

void loop() {
  long irValue = particleSensor.getIR();

  // Trigger: Sensing starts when finger is placed (IR > 20000)
  if (irValue > 20000) {
    if (!fingerDetected) {
      fingerDetected = true;
      simulationTick = 0; // Reset cycle when finger is placed
      display.clear();
      updateOLED();
    }

    // Periodic update every 1 second (Randomized logic)
    if (millis() - lastUpdate > 1000) {
      lastUpdate = millis();
      simulationTick++;

      // User Logic: Every 3 seconds trigger emergency, otherwise normal
      if (simulationTick % 3 == 0) {
        // --- EMERGENCY STATE ---
        // Range: BPM < 60 or > 80 (Alert triggers)
        // Values must still be within display bounds: 50-90
        bpm = random(81, 91); // 81-90
        
        // Range: SpO2 < 95 (Alert triggers)
        // Values must still be within display bounds: 90-100
        spo2 = random(90, 95); // 90-94
        
        // Range: Temp < 96 (Alert triggers)
        // Values must still be within display bounds: 90-100
        temp = (float)random(900, 960) / 10.0; // 90.0-95.9
      } else {
        // --- NORMAL STATE ---
        // Range: BPM 60-80
        bpm = random(60, 81);
        
        // Range: SpO2 95-100
        spo2 = random(95, 101);
        
        // Range: Temp 96-99
        temp = (float)random(960, 991) / 10.0;
      }
      
      updateOLED();
      sendToDashboards();
      
      // Voice Alerts for Emergency
      checkEmergencyAlerts();
    }
  } else {
    // Reset simulation when finger is removed
    if (fingerDetected) {
      fingerDetected = false;
      bpm = 0; spo2 = 0; temp = 0.0;
      simulationTick = 0;
      updateOLED();
      sendToDashboards();
    }
  }
}

void checkEmergencyAlerts() {
  bool emergency = false;
  
  // Alert thresholds:
  // BPM: Outside 60-80
  // SpO2: Outside 95-100
  // Temp: Outside 96-99
  if (bpm < 60 || bpm > 80) emergency = true;
  if (spo2 < 95 || spo2 > 100) emergency = true;
  if (temp < 96.0 || temp > 99.0) emergency = true;

  if (emergency) {
    // 3-second cooldown as requested (triggers every 3 seconds if finger is kept long)
    if (millis() - lastAlertTime > 3000) {
      myDFPlayer.play(2); // Play 0002.mp3 (Emergency Alert)
      lastAlertTime = millis();
    }
  }
}

void updateOLED() {
  display.setCursor(0, 0);
  display.set2X();
  display.println(F("Med-Alert"));
  display.set1X();
  display.println(F("Patient:SRIKAR"));
  display.println(F("---------------------"));
  
  display.setCursor(0, 4);
  display.print(F("BPM:  ")); 
  if (bpm > 0) display.print(bpm); else display.print(F("--"));
  display.println(F("      "));
  
  display.setCursor(0, 6);
  display.print(F("SpO2: ")); 
  if (spo2 > 0) { display.print(spo2); display.print(F(" %")); } else display.print(F("-- %"));
  display.println(F("      "));
  
  display.setCursor(0, 7);
  display.print(F("Temp: ")); 
  if (temp > 0.1) { display.print(temp, 1); display.print(F(" F")); } else display.print(F("-- F"));
  display.println(F("      "));
}

void sendToDashboards() {
  // Serial format expected by arduino_bridge.py
  Serial.print(F("BPM:")); Serial.print(bpm);
  Serial.print(F(",SPO2:")); Serial.print(spo2);
  Serial.print(F(",TEMP:")); Serial.println(temp, 1);
}

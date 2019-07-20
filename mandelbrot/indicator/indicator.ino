#include <LiquidCrystal.h>

bool jobActive = false;
int jobLedPin = 2;
int calcLedPin = 4;
char inactive[] = "No Job Running";
char jobProgress[] = "0% Complete";
String progressBar = "[              ]";
char input;
bool lightOn = false;
int blinkTime = 250;
int timeOn = 0;
int startOn = 0;
long totalJobs = -1;
long completedJobs = 0;
float jobPercentage;
String progressText;
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);


void setup() {
    pinMode(jobLedPin, OUTPUT);
    pinMode(calcLedPin, OUTPUT);
    Serial.begin(9600);
    lcd.begin(16, 2);
    lcd.clear();
    lcd.print(inactive);
}

void loop() {
  if (Serial.available()) {
    input = Serial.read();
  }
  
  if (jobActive) {
    if (lightOn == true) {
      timeOn = millis() - startOn;
      if (timeOn > blinkTime) {
        digitalWrite(calcLedPin, LOW);
        lightOn = false;
        completedJobs += 1;
        jobPercentage = float(completedJobs) / float(totalJobs) * 100;
        progressText = String(jobPercentage) + "%";
        lcd.clear();
        lcd.print(progressText);
        input = Serial.read();
      }
    } else if (input == '2') {
      digitalWrite(calcLedPin, HIGH);
      lightOn = true;
      startOn = millis();
    }

    if (input == '9'){
      jobActive = false;
      digitalWrite(jobLedPin, LOW);
      digitalWrite(calcLedPin, LOW);
      lcd.clear();
      lcd.print(inactive);
    }
  } else {
      if (input == '1'){
        while (totalJobs == -1){
          totalJobs = Serial.parseInt();
        }
        digitalWrite(jobLedPin, HIGH);
        jobActive = true;
        lcd.clear(); //Get rid of this
        lcd.print(jobProgress);
        lcd.setCursor(0, 1);
        lcd.print(progressBar);
      }
  }
}

#define pbPin 2
#define ldrPin 34
#define trigPin 4
#define echoPin 5
#define redPin 21
#define greenPin 19
#define bluePin 18
#include <WiFi.h>
#include <HTTPClient.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>


int pbValue = 0;
int ldrValue;
double good_duration;
int duration;
int status = 0;

// פרטי הרשת שלך
const char* ssid = "Escolls_248641";
const char* password = "12345678";
const char* host = "192.168.1.106";
const uint16_t port = 5001;


void setup() {
    Serial.begin(115200);
    pinMode(pbPin, INPUT_PULLUP);  // הגדרת פין הלחצן כקלט עם ניגודיות פנימית,
    pinMode(ldrPin,INPUT_PULLUP);
    pinMode(trigPin,OUTPUT);
    pinMode(echoPin,INPUT_PULLUP);
    pinMode(redPin,  OUTPUT);              
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    
    // התחברות לרשת WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

    // בדיקת כתובת IP של ה-ESP32
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
  
    pbValue = digitalRead(pbPin);
    ldrValue=analogRead(ldrPin);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // הפעלת המקלט, קריאת התוצאה
    duration = pulseIn(echoPin, HIGH);
    good_duration=duration * 343.0 / 2 / 10000;
    
    if (pbValue == HIGH) 
    { 
        while(!checkLDR() && !checkUltra());//ממתין לקבלת תוצאות טובות מהחיישנים
        status = 1 - status;
        Serial.println("Button pressed, sending POST request");
        setColor(0,  0, 255);
        sendPostRequest();
    }
    delay(1000);  // המתן שנייה לפני בדיקה מחדש
}

bool checkUltra()
{
    ldrValue=analogRead(ldrPin);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // הפעלת המקלט, קריאת התוצאה
    duration = pulseIn(echoPin, HIGH);
    good_duration=duration * 343.0 / 2 / 10000;
    Serial.println(good_duration);
    if(good_duration>=30 && good_duration<=60)
    {
      return true;
    }
    else
    {
      return false;
    }
}

bool checkLDR()
{
    ldrValue=analogRead(ldrPin);
    Serial.println(ldrValue);
    if(ldrValue>4000)
    {
      return true;
    }
    return false;
}



void sendPostRequest() {
  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  }

  // שליחה לשרת
  // המרת משתנה שלם למחרוזת
  char message[10];
  sprintf(message, "%d", status);
  client.write(message, strlen(message));
  // המתנה לקבלת תשובה מהשרת
  while (client.connected()) {
    if (client.available()) {
      String response = client.readStringUntil('\n');
      lightLed(response);
      Serial.print("Response from server: ");
      Serial.println(response);
      break;
    }
  }

  // סגירת החיבור לשרת
  client.stop();
}

void lightLed(String response)
{
  if(response=="0")
  {
    //הדלקת נורית ירוקה
    setColor(94,  255, 0);
    delay(10000);
  }
  else
  {
    if(response=="1")
    {
    //הדלקת נורית צהובה
    setColor(255,  255, 0);
    delay(10000);
    }
    else
    {
      if(response=="2")
      {
      //הדלקת נורית אדומה
        setColor(255,  0, 0);
        delay(10000);
      }
    }
  }
}

void setColor(int redValue, int greenValue,  int blueValue) {
  analogWrite(redPin, redValue);
  analogWrite(greenPin,  greenValue);
  analogWrite(bluePin, blueValue);
}

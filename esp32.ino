#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "wifiid";
const char* password = "wifipass";

WebServer server(80);

const int pinD21 = 21;
const int pinD22 = 22;
const int pinD23 = 23;

void setup() {
  Serial.begin(115200);
  pinMode(pinD21, OUTPUT);
  pinMode(pinD22, OUTPUT);
  pinMode(pinD23, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  // Looping 2x mati-nyala pada pin D21 saat pertama kali menyala
  for (int i = 0; i < 2; i++) {
    digitalWrite(pinD21, HIGH);
    delay(200);
    digitalWrite(pinD21, LOW);
    delay(200);
  }

  server.on("/", handleRoot);
  server.on("/1", handleIP1);
  server.on("/2", handleIP2);
  server.on("/3", handleIP3);
  server.on("/4", handleIP4);
  
  server.begin();
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 Control</h1>";
  html += "<button onclick=\"location.href='/1'\">Execute IP/1</button><br><br>";
  html += "<button onclick=\"location.href='/2'\">Execute IP/2</button><br><br>";
  html += "<button onclick=\"location.href='/3'\">Execute IP/3</button><br><br>";
  html += "<button onclick=\"location.href='/4'\">Execute IP/4</button><br><br>";
  html += "</body></html>";
  
  server.send(200, "text/html", html);
}

void handleIP1() {
  digitalWrite(pinD23, HIGH);
  digitalWrite(pinD22, LOW);
  for (int i = 0; i < 1; i++) {
    digitalWrite(pinD21, HIGH);
    delay(200);
    digitalWrite(pinD21, LOW);
    delay(200);
  }
  server.send(200, "text/plain", "Executed IP/1");
}

void handleIP2() {
  digitalWrite(pinD22, HIGH);
  digitalWrite(pinD23, LOW);
  server.send(200, "text/plain", "Executed IP/2");
}

void handleIP3() {
  for (int i = 0; i < 10; i++) {
    digitalWrite(pinD23, (i % 2 == 0) ? HIGH : LOW);
    digitalWrite(pinD22, (i % 2 == 0) ? LOW : HIGH);
    delay(200);
  }
  server.send(200, "text/plain", "Executed IP/3");
}

void handleIP4() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(pinD21, HIGH);
    delay(200);
    digitalWrite(pinD21, LOW);
    delay(200);
  }
  server.send(200, "text/plain", "Executed IP/4");
}

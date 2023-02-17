

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WiFiMulti.h> 
#include <ESP8266mDNS.h>
#include <ESP8266WebServer.h>

ESP8266WiFiMulti wifiMulti;     // Create an instance of the ESP8266WiFiMulti class, called 'wifiMulti'

ESP8266WebServer server(80);    // Create a webserver object that listens for HTTP request on port 80

int machine_state = 0;

const char* ssid = "FAQ";
const char* password = "244466666";
const char* dname = "station0";
IPAddress local_IP(192, 168, 0, 70);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 0, 0);
 
const int analogInPin = A0;  // ESP8266 Analog Pin ADC0 = A0
int sensorValue = 0;  // value read from the pot
int which_button(int);
int butt_num;

void handleRoot();              // function prototypes for HTTP handlers
void handleREF();
void handleNotFound();

void setup(void){
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');

  if (!WiFi.config(local_IP, gateway, subnet))
    Serial.println("STA Failed");
  wifiMulti.addAP(ssid, password);   // add Wi-Fi networks you want to connect to
  //wifiMulti.addAP("ssid_from_AP_2", "your_password_for_AP_2");
  //wifiMulti.addAP("ssid_from_AP_3", "your_password_for_AP_3");

  Serial.println("Connecting ...");
  int i = 0;
  WiFi.mode(WIFI_STA);

  while (wifiMulti.run() != WL_CONNECTED) { // Wait for the Wi-Fi to connect: scan for Wi-Fi networks, and connect to the strongest of the networks above
    delay(250);
    Serial.print('.');
  }
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());              // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // Send the IP address of the ESP8266 to the computer

  if (MDNS.begin(dname)) {              // Start the mDNS responder for esp8266.local
    Serial.println("mDNS responder started");
  } else {
    Serial.println("Error setting up MDNS responder!");
  }

  server.on("/", HTTP_GET, handleRoot);     // Call the 'handleRoot' function when a client requests URI "/"
  server.on("/REF", HTTP_POST, handleREF);  // Call the 'handleREF' function when a POST request is made to URI "/REF"
  server.onNotFound(handleNotFound);        // When a client requests an unknown URI (i.e. something other than "/"), call function "handleNotFound"

  server.begin();                           // Actually start the server
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();                    // Listen for HTTP requests from clients
  MDNS.update();
  sensorValue = analogRead(analogInPin);
  butt_num = which_button(sensorValue);
  if(butt_num>=0)
    machine_state = butt_num;
    //Serial.println(butt_num);
  Serial.print("\tMachine State: ");
  Serial.print(machine_state);
  Serial.print("\n");
  delay(50);
}

void handleRoot() {                         // When URI / is requested, send a web page with a button to toggle the LED
  String response = "Invalid State";
  response = "<form action=\"/REF\" method=\"POST\"> <input type=\"submit\" value=\"Refresh \"> </form> ";
  response = response + String(machine_state) + String(sensorValue);
  server.send(200, "text/html", response);
}

void handleREF() {                          // If a POST request is made to URI /REF
  //digitalWrite(led,!digitalRead(led));      // Change the state of the LED
  server.sendHeader("Location","/");        // Add a header to respond with a new location for the browser to go to the home page again
  server.send(303);                         // Send it back to the browser with an HTTP status 303 (See Other) to redirect
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found"); // Send HTTP status 404 (Not Found) when there's no handler for the URI in the request
}


int which_button(int s_val)
{
  // Reads ADC value and interprets which button was pressed
  Serial.print(s_val);
  if(s_val > 950)
    return 5; //9
  else if(s_val > 850)
    return 4; //8
  else if(s_val > 750)
    return 3; //7
  else if(s_val > 650)
    return 2; //6
  else if(s_val > 550)
    return 1; //5
  else if(s_val > 460)
    return 6; //4
  else if(s_val > 360)
    return 7; //3
  else if(s_val > 270)
    return 8; //2
  else if(s_val > 180)
    return 9; //1
  else if(s_val > 80)
    return 10; //0
  else
    return -1;
}

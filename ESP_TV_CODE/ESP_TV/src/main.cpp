#include <WiFi.h>
#include <TFT_eSPI.h> // Graphics library for the TFT display
#include <HTTPClient.h>

TFT_eSPI tft;

const char* ssid = "YourWiFiSSID";
const char* password = "YourWiFiPassword";
const char* serverUrl = "http://yourserver.com/image.jpg"; // Replace with your server URL

void setup() {
  tft.init();
  tft.setRotation(0);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Fetch and display the image
  fetchAndDisplayImage();
}

void loop() {
  // Your main code, if any, goes here
}

void fetchAndDisplayImage() {
  HTTPClient http;

  // Send a GET request to the server to fetch the image
  http.begin(serverUrl);

  int httpResponseCode = http.GET();
  if (httpResponseCode == 200) {
    // Successful response, get the image data
    WiFiClient& stream = http.getStream();

    // Display the image on the TFT screen
    tft.fillScreen(TFT_BLACK);
    tft.drawJpgStream(stream, 0, 0);

    // Release resources
    stream.stop();
  } else {
    Serial.print("HTTP error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

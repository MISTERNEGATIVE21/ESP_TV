// Include necessary libraries
#include <TJpg_Decoder.h>
#include <FS.h>
#ifdef ESP8266
  #include <ESP8266WiFi.h>
  #include <ESP8266HTTPClient.h>
  #include <ESP8266WiFiMulti.h>
  #include <WiFiClientSecureBearSSL.h>
#else
  #include <SPIFFS.h> // Required for ESP32 only
  #include <WiFi.h>
  #include <HTTPClient.h>
#endif
#include "SPI.h"
#include <TFT_eSPI.h>
#include "List_SPIFFS.h"
#include "Web_Fetch.h"
TFT_eSPI tft = TFT_eSPI();

// Define your WiFi credentials
#define WIFI_SSID "Rickswifi"
#define PASSWORD "ricksuvo101"

// Global variables to control image rendering
bool imageLoaded = false;
bool imageDisplayed = false;
bool imageRemoved = false;

// This function will be called during decoding of the jpeg file to render each block to the TFT
bool tft_output(int16_t x, int16_t y, uint16_t w, uint16_t h, uint16_t* bitmap)
{
  if (y >= tft.height()) return false; // Stop rendering if the image exceeds the TFT boundaries
  tft.pushImage(x, y, w, h, bitmap);
  return true; // Continue decoding
}

void setup()
{
  Serial.begin(115200);
  Serial.println("\n\n Testing TJpg_Decoder library");

  if (!SPIFFS.begin()) {
    Serial.println("SPIFFS init failed!");
    while (1) yield();
  }

  Serial.println("Start display");
  tft.begin();
  tft.fillScreen(TFT_BLACK);

  TJpgDec.setJpgScale(1);
  TJpgDec.setSwapBytes(true);
  TJpgDec.setCallback(tft_output);

  WiFi.begin(WIFI_SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();

  // Clean up any existing image
  if (SPIFFS.exists("/saved.jpg")) {
    Serial.println("Removing existing file");
    SPIFFS.remove("/saved.jpg");
  }

  // Initialize imageLoaded to true so that the first image can be fetched
  imageLoaded = true;
}

void loop()
{
  if (imageLoaded) {
    // Fetch the jpg file from the specified URL
    bool loaded_ok = getFile("http://192.168.1.4:8080/luffy.jpeg", "/saved.jpg");
    if (loaded_ok) {
      Serial.println("Image downloaded successfully");
      imageLoaded = false;
      imageDisplayed = false;
      imageRemoved = false;
    } else {
      Serial.println("Image download failed");
    }
  }

  if (!imageDisplayed && !imageRemoved) {
    // Display the downloaded image
    TJpgDec.drawFsJpg(0, 0, "/saved.jpg");
    imageDisplayed = true;
  }

  if (imageDisplayed && !imageRemoved) {
    // Add logic here to decide when to remove the image, e.g., after a certain time period
    // For example, remove the image after 2 seconds
    if (millis() > 2000) {
      SPIFFS.remove("/saved.jpg");
      imageRemoved = true;
      Serial.println("Image removed");
    }
  }

  // You can add more conditions or logic as needed to control the flow

  // Add a delay to avoid excessive loop iterations
  delay(1000);
}

#include <TFT_eSPI.h>
#include <TJpg_Decoder.h>
#include <ArduinoWebsockets.h>
#include <WiFi.h>
#include <SPI.h>

const char* ssid = "Rickswifi"; // Enter SSID
const char* password = "ricksuvo101"; // Enter Password
const char* websockets_server_host = "192.168.1.4"; // Enter server address
const uint16_t websockets_server_port = 8888; // Enter server port

#define FRAMESIZE_QQVGA_WIDTH  160
#define FRAMESIZE_QQVGA_HEIGHT 128

using namespace websockets;
TFT_eSPI tft = TFT_eSPI();
WebsocketsClient client;

bool tft_output(int16_t x, int16_t y, uint16_t w, uint16_t h, uint16_t* bitmap)
{
  // Stop further decoding as the image is running off the bottom of the screen
  if (y >= tft.height()) return 0;

  // This function will clip the image block rendering automatically at the TFT boundaries
  tft.pushImage(x, y, w, h, bitmap);

  // Return 1 to decode the next block
  return 1;
}

void setup()
{
  tft.begin();
  tft.setRotation(3);
  tft.setTextColor(0xFFFF, 0x0000);
  tft.fillScreen(TFT_RED);
  tft.setSwapBytes(true); // We need to swap the color bytes (endianess)

  // The JPEG image can be scaled by a factor of 1, 2, 4, or 8
  TJpgDec.setJpgScale(1);

  // The decoder must be given the exact name of the rendering function above
  TJpgDec.setCallback(tft_output);
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);

  // Wait some time to connect to Wi-Fi
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(1000);
  }

  // Check if connected to Wi-Fi
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("No WiFi!");
    return;
  }

  Serial.println("Connected to WiFi, Connecting to server.");
  
  // Try to connect to WebSocket server
  bool connected = client.connect(websockets_server_host, websockets_server_port, "/");
  
  if (connected)
  {
    Serial.println("Connected!");
    client.send("Hello Server");
  }
  else
  {
    Serial.println("Not Connected!");
  }

  // Run callback when messages are received
  client.onMessage([&](WebsocketsMessage message)
  {
    Serial.print("Got Message: ");
    Serial.println(message.data());

    // Decode and display the JPEG image on the TFT display
    String data = message.data();
    uint16_t w = 0, h = 0;
    TJpgDec.getJpgSize(&w, &h, (const uint8_t*)data.c_str(), data.length());
    Serial.print("Width = "); Serial.print(w); Serial.print(", height = "); Serial.println(h);
    TJpgDec.drawJpg(0, 0, (const uint8_t*)data.c_str(), data.length());
  });
}

void loop()
{
  if (client.available())
  { delay(5000);
    client.poll();
  }
}

#include <Arduino.h>

/*
 Adapted from the Adafruit graphicstest sketch, see orignal header at end
 of sketch.

 This sketch uses the GLCD font (font 1) only.

 Make sure all the display driver and pin comnenctions are correct by
 editting the User_Setup.h file in the TFT_eSPI library folder.

 #########################################################################
 ###### DON'T FORGET TO UPDATE THE User_Setup.h FILE IN THE LIBRARY ######
 #########################################################################
*/

#include <SPIFFS.h>
#include <ArduinoWebsockets.h>
#include <WiFi.h>
#include "SPI.h"
#include "TFT_eSPI.h"
#include <TJpg_Decoder.h>

TFT_eSPI tft = TFT_eSPI();

const char* ssid = "Red Wifi";
const char* password = "Clave Wifi";

const char* imageFileName = "/camimage.jpeg";

IPAddress IP(192,168,4,1);     
IPAddress gateway(192,168,4,1);   
IPAddress subnet(255,255,255,0);   


using namespace websockets;
WebsocketsServer server;
WebsocketsClient client;
boolean SDInited = false;

bool tft_output(int16_t x, int16_t y, uint16_t w, uint16_t h, uint16_t* bitmap)
{
   // Stop further decoding as image is running off bottom of screen
  if ( y >= tft.height() ) return 0;

  // This function will clip the image block rendering automatically at the TFT boundaries
  tft.pushImage(x, y, w, h, bitmap);

  // This might work instead if you adapt the sketch to use the Adafruit_GFX library
  // tft.drawRGBBitmap(x, y, bitmap, w, h);

  // Return 1 to decode next block
  return 1;
}


boolean fileWrite(String name, WebsocketsMessage content){
  String strEntrada = content.c_str(); 
  byte bytEntrada0 = strEntrada[0];
  byte bytEntrada1 = strEntrada[1];
  byte bytEntrada2 = strEntrada[2];
  byte bytEntrada3 = strEntrada[3];
  // Encabezado jpg
  if (bytEntrada0 == 255 && bytEntrada1 == 216 && bytEntrada2 == 255 && bytEntrada3 == 224  ){
    File file = SPIFFS.open(name.c_str(), "w");
    if(!file){
      String errorMsg = "Can't open file";
      Serial.println(errorMsg);
      return false;
    }else{
      file.write((const uint8_t*) content.c_str(), content.length());
      Serial.print("Escribio jpg " + name);
      file.close();
      return true;
    }
  }
  else{
    return false;
  }
}

void setup(void) {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  
  if(!SPIFFS.begin(true)){
    Serial.println("SPIFFS init failed!");
    while(1) yield();
  }else{
    SDInited = true;
  } 

  Serial.println("Espere 30 segundos para que se formatee el SPIFFS"); 
  SPIFFS.format();
  Serial.println("Spiffs formateado"); 

  Serial.println("Arrancando el display");
  
  tft.begin();
  tft.setRotation(1);
  tft.setTextColor(0xFFFF, 0x0000);
  tft.fillScreen(TFT_BLUE);
  tft.setSwapBytes(true); // We need to swap the colour bytes (endianess)

  // The jpeg image can be scaled by a factor of 1, 2, 4, or 8
  TJpgDec.setJpgScale(1);

  // The decoder must be given the exact name of the rendering function above
  TJpgDec.setCallback(tft_output);
  
  Serial.println();
  Serial.println("Setting AP...");//  WiFi.softAP(ssid, password);

//  IPAddress IP = WiFi.softAPIP();

  WiFi.mode(WIFI_STA);
  WiFi.config(IP, gateway, subnet);
  WiFi.begin(ssid, password);
  
  Serial.print("AP IP Address : ");
  Serial.println(IP);
  tft.fillScreen(TFT_BLUE);
  tft.print(IP);
  server.listen(8888);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(SDInited){
    if(server.poll()){
      client = server.accept();
    }

    if(client.available()){
      client.poll();
      Serial.print("Entro el cliente");
      WebsocketsMessage msg = client.readBlocking();
      boolean isSaved = fileWrite(imageFileName, msg);
      Serial.print(isSaved);
      if(isSaved){
        
        uint32_t t = millis();

        // Get the width and height in pixels of the jpeg if you wish
        uint16_t w = 0, h = 0;
        TJpgDec.getFsJpgSize(&w, &h, imageFileName); // Note name preceded with "/"
        Serial.print("Width = "); Serial.print(w); Serial.print(", height = "); Serial.println(h);
      
        // Draw the image, top left at 0,0
        TJpgDec.drawFsJpg(0, 0, imageFileName);
      
        // How much time did rendering take (ESP8266 80MHz 271ms, 160MHz 157ms, ESP32 SPI 120ms, 8bit parallel 105ms
        t = millis() - t;
        Serial.print(t); Serial.println(" ms");
      }
    }
  }
}

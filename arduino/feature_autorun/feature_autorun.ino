
#include "DHT.h"
#include <Bridge.h>
#include <FileIO.h>
#define DHTPIN A0     // what pin we're connected to
#define DHTTYPE DHT11   // DHT 11 
DHT dht(DHTPIN, DHTTYPE);
#include <Wire.h>;
#include <ADXL345.h>

ADXL345 adxl; //variable adxl is an instance of the ADXL345 library
long time;
double ax,ay,az;



#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(8, 7);
Adafruit_GPS GPS(&mySerial);



// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO  false

boolean usingInterrupt = false;
void useInterrupt(boolean);
// Context broker config
String CB_SCRIPT = "python /mnt/sda1/marbellawork/email_feature.py";



void setup()  
{
  Bridge.begin();
  
  dht.begin();
  
  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  Serial.begin(115200);
  delay(5000);
  Serial.println("Arranca Script Linux");
  
  runScript();
  Serial.println("Adafruit GPS library basic test!");

  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);
  
  /*Configuracion del sensor del acelerometro */
  adxl.powerOn();
  //look of activity movement on this axes - 1 == on; 0 == off 
  adxl.setActivityX(1);
  adxl.setActivityY(1);
  adxl.setActivityZ(1);
  
  
}

uint32_t timer = millis();
void loop()                     // run over and over again
{
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if ((c) && (GPSECHO))
    Serial.write(c); 
  
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis())  timer = millis();

  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 2000) { 
    timer = millis(); // reset the timer
    
    Serial.print("\nTime: ");
    Serial.print(GPS.hour, DEC); Serial.print(':');
    Serial.print(GPS.minute, DEC); Serial.print(':');
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    Serial.println(GPS.milliseconds);
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
    Serial.print("Fix: "); Serial.print((int)GPS.fix);
    Serial.print(" quality: "); Serial.println((int)GPS.fixquality); 
    readAndSendSensors();
        
  }
}


void readAndSendSensors(){
  
  
  if (GPS.fix) {
  float lat,lon, high,spd;
  
  lat = GPS.latitude;
  lon = GPS.longitude;
  spd = (GPS.speed)*1.852; // nudos a kph
  
  if (GPS.lat== 'N'){
    lat = GPS.latitude;
  }else{
    lat = -(GPS.latitude);
  }
  if (GPS.lon== 'E'){
    lon = GPS.longitude;
  }else{
    lon = -(GPS.longitude);
  }
  high = GPS.altitude; 
   
  Serial.print("Velocidad: ");
  Serial.println (spd);
  Serial.print("Longitud: ");
  Serial.print (GPS.longitude);
  Serial.println(GPS.lon);
  Serial.print("Latitud: ");
  Serial.print (GPS.latitude);
  Serial.println(GPS.lat);
  Serial.print("Altura: ");
  Serial.println (high);
  Bridge.put("speed",String(spd));
  Bridge.put("longitude",String(lon));
  Bridge.put("latitude",String(lat));
  Bridge.put("high",String(high));
  }
  
  
  float h,t;
  h = dht.readHumidity();
  t = dht.readTemperature();
  ax, ay, az = getTilt();
  /*Envio de los sensores al Linux */
  
  Bridge.put("temperature",String(t));
  Bridge.put("humidity",String(h));
  //Bridge.put("distance",String(d));
  Bridge.put("xtilt",String(ax));
  Bridge.put("ytilt",String(ay));
  Bridge.put("ztilt",String(az));
  
}

float getTilt(){
  double xyz[3];
  
  adxl.getAcceleration(xyz);      
  ax = xyz[0]*100;
  ay = xyz[1]*100;
  az = xyz[2]*100;
  
  return ax, ay , az;
}


void runScript() {
  // Run the script and show results on the Serial
  Process sendContextBroker;
  sendContextBroker.runShellCommandAsynchronously(CB_SCRIPT);      
   
}





